#!/usr/bin/env python3
"""
DHT11 reader for the Raspberry Pi 5 (RP1) using lgpio edge timestamps.

The kernel timestamps every edge on the data line, so Python scheduling
jitter never touches the pulse widths. What matters is (1) arming the edge
capture quickly after the start pulse and (2) decoding tolerantly.

Usage:
    python dht11_edges.py bench              # 30 raw reads + statistics
    python dht11_edges.py bench --count 100
    python dht11_edges.py bench --dump       # also print the raw edges of failed reads
    python dht11_edges.py run                # continuous; retries bad frames
    python dht11_edges.py selftest           # decoder test, no hardware needed

    --chip N   gpiochip of the RP1 (run `gpiodetect`, pick "pinctrl-rp1")
    --pin N    BCM GPIO number wired to the DHT11 data line
"""
import argparse
import gc
import random
import sys
import textwrap
import threading
import time
from collections import Counter
from dataclasses import dataclass, field
from typing import Optional

try:
    import lgpio
except ImportError:  # lets `selftest` run on a machine without lgpio
    lgpio = None

# ------------------------------------------------------------------ settings
CHIP = 15                # RP1 gpiochip number on your system
PIN = 5                  # BCM GPIO connected to the DHT11 data line

START_LOW_S = 0.020      # host start pulse (datasheet minimum is 18 ms)
FRAME_WINDOW_S = 0.010   # a frame lasts ~5 ms on the wire; listen for 10 ms
MIN_PERIOD_S = 1.1       # DHT11 needs >= 1 s between reads
LATE_ARM_US = 250.0      # first data bit starts ~240 us after the line is released

# DHT11 high-pulse widths in microseconds: response ~80, bit 0 ~27, bit 1 ~70
BIT_THRESHOLD_US = 48.0              # midpoint between 27 and 70
PULSE_MIN_US, PULSE_MAX_US = 10.0, 120.0
RESPONSE_MIN_US, RESPONSE_MAX_US = 60.0, 120.0


# ------------------------------------------------------------------ decoding
class DecodeError(Exception):
    def __init__(self, kind, detail=""):
        super().__init__(f"{kind}: {detail}" if detail else kind)
        self.kind = kind
        self.detail = detail


def high_pulse_widths_us(edges):
    """edges: [(timestamp_ns, level), ...] -> widths (us) of each rise->fall pair."""
    widths = []
    for (t1, lvl1), (t2, lvl2) in zip(edges, edges[1:]):
        if lvl1 == 1 and lvl2 == 0 and t2 > t1:
            widths.append((t2 - t1) / 1000.0)
    return widths


def response_seen(widths):
    """True if the ~80 us sensor response pulse sits just before the 40 data pulses."""
    return len(widths) >= 41 and RESPONSE_MIN_US <= widths[-41] <= RESPONSE_MAX_US


def decode_widths(widths):
    """Return (humidity, temperature) or raise DecodeError.

    Uses the LAST 40 high pulses, so it still works when the capture started
    late and missed the sensor's response pulse.
    """
    if len(widths) < 40:
        raise DecodeError("few_pulses", f"{len(widths)} high pulses, need 40")

    bits = []
    for w in widths[-40:]:
        if not PULSE_MIN_US <= w <= PULSE_MAX_US:
            raise DecodeError("bad_width", f"{w:.0f} us pulse")
        # Classify by nearest nominal width. No "ambiguous" dead zone: the
        # checksum below catches genuine mistakes.
        bits.append(1 if w > BIT_THRESHOLD_US else 0)

    raw = [int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, 40, 8)]
    h_int, h_dec, t_int, t_dec, checksum = raw

    if ((h_int + h_dec + t_int + t_dec) & 0xFF) != checksum:
        raise DecodeError("checksum", f"got 0x{checksum:02X}")

    # A DHT11's decimal bytes are always 0, so a larger value means corrupted
    # data that happened to pass the checksum.
    if h_dec > 9 or t_dec > 9:
        raise DecodeError("implausible", "decimal byte > 9")

    humidity = h_int + h_dec / 10.0
    temperature = t_int + t_dec / 10.0
    if not (0.0 <= humidity <= 100.0 and -20.0 <= temperature <= 60.0):
        raise DecodeError("implausible", f"H={humidity} T={temperature}")
    return humidity, temperature


# ------------------------------------------------------------------- sensor
@dataclass
class Result:
    humidity: Optional[float] = None
    temperature: Optional[float] = None
    error: Optional[str] = None      # None when valid, else the failure kind
    detail: str = ""
    edges: int = 0
    pulses: int = 0
    response: bool = False
    gap_us: float = 0.0              # release -> edge capture armed
    max_edge_gap_us: float = 0.0     # longest pause between captured edges
    raw: list = field(default_factory=list)   # [(level, us since previous edge), ...]
    elapsed_ms: float = 0.0

    @property
    def ok(self):
        return self.error is None


class Dht11:
    def __init__(self, chip, pin):
        self.pin = pin
        self._lock = threading.Lock()
        self._edges = []
        self._armed = False
        self.handle = lgpio.gpiochip_open(chip)
        rc = lgpio.gpio_claim_alert(self.handle, pin, lgpio.BOTH_EDGES, lgpio.SET_PULL_UP)
        if rc < 0:
            raise RuntimeError(f"cannot monitor GPIO{pin}: {rc}")
        self._cb = lgpio.callback(self.handle, pin, lgpio.BOTH_EDGES, self._on_edge)

    def _on_edge(self, chip, gpio, level, timestamp):
        if self._armed and level in (0, 1):      # level 2 = watchdog, ignore
            with self._lock:
                self._edges.append((timestamp, level))

    def _safe_free(self):
        try:
            lgpio.gpio_free(self.handle, self.pin)
        except lgpio.error:
            pass

    def read_once(self):
        """One raw attempt. Never raises DecodeError; returns a Result."""
        h, pin = self.handle, self.pin
        free, claim_out, claim_alert = lgpio.gpio_free, lgpio.gpio_claim_output, lgpio.gpio_claim_alert
        both, pull_up = lgpio.BOTH_EDGES, lgpio.SET_PULL_UP
        now_ns = time.perf_counter_ns
        t_start = now_ns()

        with self._lock:
            self._edges.clear()

        # Start pulse: drive the line low.
        self._safe_free()
        rc = claim_out(h, pin, 0)
        if rc < 0:
            raise RuntimeError(f"cannot drive GPIO{pin} low: {rc}")
        time.sleep(START_LOW_S)

        # Release the line and start timestamping as fast as possible. The
        # sensor answers ~30 us later and the first data bit starts roughly
        # 240 us after release, so every microsecond here counts.
        gc.disable()
        try:
            self._armed = True
            t0 = now_ns()
            free(h, pin)
            rc = claim_alert(h, pin, both, pull_up)
            gap_us = (now_ns() - t0) / 1000.0
        finally:
            gc.enable()
        if rc < 0:
            self._armed = False
            raise RuntimeError(f"cannot monitor GPIO{pin}: {rc}")

        time.sleep(FRAME_WINDOW_S)
        self._armed = False
        with self._lock:
            edges = list(self._edges)

        widths = high_pulse_widths_us(edges)
        intervals = [(b[0] - a[0]) / 1000.0 for a, b in zip(edges, edges[1:])]
        result = Result(edges=len(edges), pulses=len(widths),
                        response=response_seen(widths), gap_us=gap_us,
                        max_edge_gap_us=max(intervals, default=0.0),
                        raw=[(lvl, 0.0 if i == 0 else intervals[i - 1])
                             for i, (_, lvl) in enumerate(edges)])
        if not edges:
            result.error, result.detail = "no_edges", "sensor never answered"
        else:
            try:
                result.humidity, result.temperature = decode_widths(widths)
            except DecodeError as exc:
                result.error, result.detail = exc.kind, exc.detail
                if exc.kind == "few_pulses" and gap_us > LATE_ARM_US:
                    result.error = "late_arm"
                    result.detail = f"armed {gap_us:.0f} us after release; {exc.detail}"
        result.elapsed_ms = (now_ns() - t_start) / 1e6
        return result

    def close(self):
        try:
            self._cb.cancel()
        except Exception:
            pass
        self._safe_free()
        try:
            lgpio.gpiochip_close(self.handle)
        except Exception:
            pass


# --------------------------------------------------------------------- modes
def safe_read(sensor):
    try:
        return sensor.read_once()
    except (lgpio.error, RuntimeError) as exc:
        return Result(error="gpio_error", detail=str(exc))


def describe(n, total, r):
    line = (f"{n:02}/{total} | {r.elapsed_ms:6.1f} ms | gap {r.gap_us:4.0f} us | "
            f"edges {r.edges:2d} | pulses {r.pulses:2d} | ")
    if r.ok:
        return line + f"H={r.humidity:.0f}%  T={r.temperature:.1f} C"
    return line + f"INVALID ({r.error}: {r.detail}; longest edge gap {r.max_edge_gap_us:.0f} us)"


def format_raw(raw):
    """R/F = new level, +N = microseconds since the previous edge, * = level repeated."""
    tokens, prev = [], None
    for level, interval in raw:
        repeat = "*" if prev is not None and level == prev else ""
        tokens.append(f"{'R' if level else 'F'}+{interval:.0f}{repeat}")
        prev = level
    return textwrap.fill(" ".join(tokens), width=100,
                         initial_indent="    ", subsequent_indent="    ")


def bench(sensor, attempts, dump=False):
    print(f"Benchmark: {attempts} raw reads on BCM GPIO{sensor.pin}\n")
    results = []
    next_start = time.monotonic()
    for n in range(1, attempts + 1):
        wait = next_start - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        started = time.monotonic()
        r = safe_read(sensor)
        next_start = started + MIN_PERIOD_S
        results.append(r)
        print(describe(n, attempts, r))
        if dump and not r.ok and r.raw:
            print(format_raw(r.raw))
    summarize(results)


def summarize(results):
    total = len(results)
    good = [r for r in results if r.ok]
    failures = Counter(r.error for r in results if not r.ok)

    print("\n--- Summary ---")
    print(f"Attempts:      {total}")
    print(f"Valid frames:  {len(good)} ({100 * len(good) / total:.0f}%)")
    for kind, count in failures.most_common():
        print(f"  {kind:<12} {count}")

    timed = [r for r in results if r.gap_us]
    if timed:
        gaps = [r.gap_us for r in timed]
        times = [r.elapsed_ms for r in timed]
        print(f"Arm gap:       avg {sum(gaps) / len(gaps):.0f} us, max {max(gaps):.0f} us "
              f"(first data bit starts ~240 us after release)")
        print(f"Read time:     avg {sum(times) / len(times):.1f} ms, "
              f"fastest {min(times):.1f}, slowest {max(times):.1f}")
        print("Pulse counts:  " + ", ".join(
            f"{p} pulses x{c}" for p, c in sorted(Counter(r.pulses for r in timed).items(), reverse=True)))
    if good:
        hs = [r.humidity for r in good]
        ts = [r.temperature for r in good]
        print(f"Humidity:      {min(hs):.0f}-{max(hs):.0f} %")
        print(f"Temperature:   {min(ts):.1f}-{max(ts):.1f} C")

    # Hints, based on which failures occurred.
    if failures.get("late_arm"):
        worst = max(r.gap_us for r in results)
        print(f"\nHint: {failures['late_arm']} read(s) stalled between releasing the line and arming "
              f"the capture (worst {worst:.0f} us; the budget is ~240 us). Stalls of milliseconds "
              "usually mean the CPU was busy with something else. Close other programs or try "
              "real-time priority. Wiring the data line to a second GPIO (one drives the start "
              "pulse, the other is permanently monitored) removes this window entirely.")
    if failures.get("few_pulses") or failures.get("no_edges"):
        print("\nHint: some frames lost pulses even though the arm gap was short. Check "
              "'longest edge gap' on those lines: under ~150 us means the frame was intact but "
              "started late; a larger value means edges were lost mid-frame.")
    if failures.get("bad_width") or failures.get("checksum"):
        print("\nHint: pulses arrived but were distorted. Check the pull-up resistor, wire "
              "length and connections, and that the sensor has a stable supply.")


def run(sensor, retries=3):
    next_start = time.monotonic()
    while True:
        for _ in range(retries):
            wait = next_start - time.monotonic()
            if wait > 0:
                time.sleep(wait)
            started = time.monotonic()
            r = safe_read(sensor)
            next_start = started + MIN_PERIOD_S
            if r.ok:
                f = r.temperature * 9 / 5 + 32
                print(f"humidity: {r.humidity:.0f} %,  temperature: {r.temperature:.1f} C / {f:.1f} F")
                break
        else:
            print(f"no valid reading after {retries} tries (last: {r.error})")


# ------------------------------------------------------------------ selftest
def synth_edges(h, t, jitter_us=0.0, drop_first=0, rng=None):
    """Build the edge list a DHT11 produces after the host releases the line.

    Edge 1: response low starts; 2: response high; 3: bit 1 low; then a rise
    and a fall for each of the 40 bits; last: sensor releases the line.
    drop_first=k removes the first k edges (simulates arming late).
    """
    rng = rng or random.Random(0)
    payload = [h, 0, t, 0, (h + t) & 0xFF]
    bits = [(byte >> i) & 1 for byte in payload for i in range(7, -1, -1)]

    clock = 30.0
    events = [(clock, 0)]
    clock += 80
    events.append((clock, 1))
    clock += 80
    events.append((clock, 0))
    for b in bits:
        clock += 50
        events.append((clock, 1))
        clock += 70 if b else 27
        events.append((clock, 0))
    clock += 50
    events.append((clock, 1))

    edges, prev = [], 0
    for t_us, level in events:
        ts = max(int((1e9 + t_us * 1000) + rng.gauss(0, jitter_us) * 1000), prev + 1)
        edges.append((ts, level))
        prev = ts
    return edges[drop_first:]


def selftest():
    failures = 0

    def check(name, cond):
        nonlocal failures
        print(f"{'PASS' if cond else 'FAIL'}  {name}")
        failures += 0 if cond else 1

    # Clean frames decode exactly.
    check("clean frame decodes", decode_widths(high_pulse_widths_us(synth_edges(67, 20))) == (67.0, 20.0))

    # Late arming: missing the response edges is fine, missing bit 1 is not.
    for k in range(4):
        widths = high_pulse_widths_us(synth_edges(55, 23, drop_first=k))
        check(f"first {k} edges missed -> still decodes", decode_widths(widths) == (55.0, 23.0))
    try:
        decode_widths(high_pulse_widths_us(synth_edges(55, 23, drop_first=4)))
        check("bit 1 rising edge missed -> rejected", False)
    except DecodeError as exc:
        check("bit 1 rising edge missed -> rejected", exc.kind == "few_pulses")

    # Corruption must be rejected, never returned as a wrong value.
    edges = synth_edges(67, 20)
    bad = [(ts + (30_000 if i == 20 else 0), lvl) for i, (ts, lvl) in enumerate(edges)]
    try:
        decode_widths(high_pulse_widths_us(bad))
        check("corrupted frame rejected", False)
    except DecodeError:
        check("corrupted frame rejected", True)

    # Timestamp jitter: every accepted value must be right.
    rng = random.Random(1234)
    ok = wrong = rejected = 0
    for _ in range(2000):
        h, t = rng.randint(20, 90), rng.randint(0, 50)
        try:
            got = decode_widths(high_pulse_widths_us(synth_edges(h, t, jitter_us=3.0, rng=rng)))
            ok, wrong = (ok + 1, wrong) if got == (float(h), float(t)) else (ok, wrong + 1)
        except DecodeError:
            rejected += 1
    check(f"2000 frames with 3 us jitter: {ok} ok, {rejected} rejected, {wrong} wrong", wrong == 0 and ok >= 1980)

    print("\nAll tests passed." if not failures else f"\n{failures} test(s) FAILED.")
    return 1 if failures else 0


# ---------------------------------------------------------------------- main
def main():
    parser = argparse.ArgumentParser(description="DHT11 reader using lgpio edge timestamps")
    parser.add_argument("mode", nargs="?", default="bench", choices=["bench", "run", "selftest"])
    parser.add_argument("--chip", type=int, default=CHIP)
    parser.add_argument("--pin", type=int, default=PIN)
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--dump", action="store_true", help="print raw edges of failed reads")
    args = parser.parse_args()

    if args.mode == "selftest":
        return selftest()
    if lgpio is None:
        sys.exit("lgpio is not available in this Python environment")

    sensor = Dht11(args.chip, args.pin)
    try:
        bench(sensor, args.count, args.dump) if args.mode == "bench" else run(sensor)
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        sensor.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())