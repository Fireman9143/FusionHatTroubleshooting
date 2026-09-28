'''Looking at more in depth testing with arduino'''

from fusion_hat.pin import Pin, Mode
import time


# ------------------------------------------------------------
# Pins
# ------------------------------------------------------------

SDI = Pin(17, mode=Mode.OUT)      # 595 pin 14 DS
SRCLK = Pin(27, mode=Mode.OUT)    # 595 pin 11 SHCP
RCLK = Pin(4, mode=Mode.OUT)      # 595 pin 12 STCP


WAIT = 10


# ------------------------------------------------------------
# Basic helpers
# ------------------------------------------------------------

def all_low():
    SDI.low()
    SRCLK.low()
    RCLK.low()


def clock_once():
    SRCLK.high()
    time.sleep(0.5)

    SRCLK.low()
    time.sleep(0.5)


def latch():
    RCLK.high()
    time.sleep(0.5)

    RCLK.low()
    time.sleep(0.5)


def shift_bits(bits, clock_delay=0.5):
    for bit in bits:

        if bit:
            SDI.high()
        else:
            SDI.low()

        # Give DATA plenty of time to settle
        time.sleep(clock_delay)

        SRCLK.high()
        time.sleep(clock_delay)

        SRCLK.low()
        time.sleep(clock_delay)


def wait_stage(seconds=WAIT):
    print()
    print(f"*** WATCH LEDs / SERIAL MONITOR FOR {seconds} SECONDS ***")
    print()
    time.sleep(seconds)


# ------------------------------------------------------------
# Start
# ------------------------------------------------------------

print()
print("========================================")
print(" SN74HC595 DIAGNOSTIC TEST")
print("========================================")
print()

all_low()
time.sleep(2)


# ============================================================
# TEST 1
# ============================================================

print("TEST 1: ALL OUTPUTS OFF")
print("------------------------")
print("Sending: 00000000")
print("Then LATCH")

shift_bits([0, 0, 0, 0, 0, 0, 0, 0])
latch()

wait_stage()


# ============================================================
# TEST 2
# ============================================================

print("TEST 2: ALL OUTPUTS ON")
print("-----------------------")
print("Sending: 11111111")
print("Then LATCH")

shift_bits([1, 1, 1, 1, 1, 1, 1, 1])
latch()

wait_stage()


# ============================================================
# TEST 3
# ============================================================

print("TEST 3: 10101010")
print("-----------------")
print("Sending: 10101010")
print("Then LATCH")

shift_bits([1, 0, 1, 0, 1, 0, 1, 0])
latch()

wait_stage()


# ============================================================
# TEST 4
# ============================================================

print("TEST 4: 01010101")
print("-----------------")
print("Sending: 01010101")
print("Then LATCH")

shift_bits([0, 1, 0, 1, 0, 1, 0, 1])
latch()

wait_stage()


# ============================================================
# TEST 5
# ============================================================

print("TEST 5: WALKING ONE")
print("--------------------")
print("One HIGH bit moves through the register.")
print()

walking_one = [
    [1,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0],
    [0,0,0,1,0,0,0,0],
    [0,0,0,0,1,0,0,0],
    [0,0,0,0,0,1,0,0],
    [0,0,0,0,0,0,1,0],
    [0,0,0,0,0,0,0,1],
]

for bits in walking_one:

    print("Sending:", "".join(str(x) for x in bits))

    shift_bits(bits)
    latch()

    wait_stage()


# ============================================================
# TEST 6
# ============================================================

print("TEST 6: WALKING ONE REVERSE")
print("----------------------------")

walking_reverse = [
    [0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,1,0],
    [0,0,0,0,0,1,0,0],
    [0,0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0,0],
    [0,0,1,0,0,0,0,0],
    [0,1,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0],
]

for bits in walking_reverse:

    print("Sending:", "".join(str(x) for x in bits))

    shift_bits(bits)
    latch()

    wait_stage()


# ============================================================
# TEST 7
# ============================================================

print("TEST 7: SHIFT WITHOUT LATCH")
print("----------------------------")

print("First: 11111111 + LATCH")
shift_bits([1,1,1,1,1,1,1,1])
latch()

print("LEDs should ALL be ON.")
wait_stage()


print("Now shifting 00000000 WITHOUT LATCH.")
shift_bits([0,0,0,0,0,0,0,0])

print("LEDs should STILL be ON.")
wait_stage()


print("Now LATCHING.")
latch()

print("LEDs should now ALL be OFF.")
wait_stage()


# ============================================================
# TEST 8
# ============================================================

print("TEST 8: RECOGNIZABLE PATTERNS")
print("------------------------------")

patterns = [
    [1,0,0,0,0,0,0,1],   # 81
    [1,1,0,0,0,0,1,1],   # C3
    [1,0,1,0,0,1,0,1],   # A5
]

for bits in patterns:

    print()
    print("Sending:", "".join(str(x) for x in bits))

    shift_bits(bits)
    latch()

    wait_stage()


# ============================================================
# Finish
# ============================================================

print()
print("========================================")
print(" DIAGNOSTIC COMPLETE")
print("========================================")
print()

all_low()

SDI.close()
SRCLK.close()
RCLK.close()


'''
All of the leds stayed lit throughout the test.  Here is the arduino data:

==========================
======================================
 SN74HC595 DIAGNOSTIC MONITOR
======================================
D2 = DATA
D3 = CLOCK
D4 = LATCH
D5 = Q7'

Waiting for Pi...

LATCH -> 0
CLOCK 1: DATA=1  Q7'=1  LATCH=0
CLOCK 2: DATA=1  Q7'=1  LATCH=0
CLOCK 3: DATA=1  Q7'=1  LATCH=0
LATCH -> 1
LATCH -> 0
CLOCK 4: DATA=1  Q7'=1  LATCH=0
CLOCK 5: DATA=1  Q7'=1  LATCH=0
LATCH -> 1
LATCH -> 0
CLOCK 6: DATA=1  Q7'=1  LATCH=0
CLOCK 7: DATA=1  Q7'=1  LATCH=0
LATCH -> 1
LATCH -> 0
CLOCK 8: DATA=1  Q7'=1  LATCH=0
CLOCK 9: DATA=1  Q7'=1  LATCH=0
CLOCK 10: DATA=1  Q7'=1  LATCH=0
CLOCK 11: DATA=1  Q7'=1  LATCH=0
CLOCK 12: DATA=1  Q7'=1  LATCH=0
CLOCK 13: DATA=1  Q7'=1  LATCH=0
CLOCK 14: DATA=1  Q7'=1  LATCH=0
CLOCK 15: DATA=1  Q7'=1  LATCH=0
CLOCK 16: DATA=1  Q7'=1  LATCH=0
CLOCK 17: DATA=1  Q7'=1  LATCH=0
CLOCK 18: DATA=1  Q7'=1  LATCH=0
CLOCK 19: DATA=1  Q7'=1  LATCH=0
CLOCK 20: DATA=1  Q7'=1  LATCH=0
CLOCK 21: DATA=1  Q7'=1  LATCH=0
LATCH -> 1
CLOCK 22: DATA=1  Q7'=1  LATCH=1
LATCH -> 0
CLOCK 23: DATA=1  Q7'=1  LATCH=0
CLOCK 24: DATA=1  Q7'=1  LATCH=0
CLOCK 25: DATA=1  Q7'=1  LATCH=0
CLOCK 26: DATA=1  Q7'=1  LATCH=0
CLOCK 27: DATA=1  Q7'=1  LATCH=0
LATCH -> 1
LATCH -> 0
CLOCK 28: DATA=1  Q7'=1  LATCH=0
CLOCK 29: DATA=1  Q7'=1  LATCH=0
CLOCK 30: DATA=1  Q7'=1  LATCH=0
CLOCK 31: DATA=1  Q7'=1  LATCH=0
CLOCK 32: DATA=1  Q7'=1  LATCH=0
CLOCK 33: DATA=1  Q7'=1  LATCH=0
CLOCK 34: DATA=1  Q7'=1  LATCH=0
CLOCK 35: DATA=0  Q7'=1  LATCH=0
LATCH -> 1
CLOCK 36: DATA=1  Q7'=1  LATCH=1
CLOCK 37: DATA=1  Q7'=1  LATCH=1
CLOCK 38: DATA=1  Q7'=1  LATCH=1
LATCH -> 0
CLOCK 39: DATA=1  Q7'=1  LATCH=0
CLOCK 40: DATA=1  Q7'=1  LATCH=0
CLOCK 41: DATA=1  Q7'=1  LATCH=0
CLOCK 42: DATA=1  Q7'=1  LATCH=0
CLOCK 43: DATA=1  Q7'=1  LATCH=0
CLOCK 44: DATA=1  Q7'=1  LATCH=0
CLOCK 45: DATA=1  Q7'=1  LATCH=0
CLOCK 46: DATA=1  Q7'=1  LATCH=0
LATCH -> 1
CLOCK 47: DATA=1  Q7'=1  LATCH=1
LATCH -> 0
CLOCK 48: DATA=1  Q7'=1  LATCH=0
CLOCK 49: DATA=1  Q7'=1  LATCH=0
CLOCK 50: DATA=1  Q7'=1  LATCH=0
CLOCK 51: DATA=1  Q7'=1  LATCH=0
CLOCK 52: DATA=1  Q7'=1  LATCH=0
CLOCK 53: DATA=1  Q7'=1  LATCH=0
CLOCK 54: DATA=1  Q7'=1  LATCH=0
CLOCK 55: DATA=1  Q7'=1  LATCH=0
LATCH -> 1
LATCH -> 0
CLOCK 56: DATA=0  Q7'=1  LATCH=0
CLOCK 57: DATA=1  Q7'=1  LATCH=0
CLOCK 58: DATA=0  Q7'=1  LATCH=0
CLOCK 59: DATA=1  Q7'=1  LATCH=0
CLOCK 60: DATA=1  Q7'=1  LATCH=0
CLOCK 61: DATA=1  Q7'=1  LATCH=0
LATCH -> 1
CLOCK 62: DATA=1  Q7'=1  LATCH=1
LATCH -> 0
CLOCK 63: DATA=1  Q7'=1  LATCH=0
CLOCK 64: DATA=1  Q7'=1  LATCH=0
LATCH -> 1
LATCH -> 0
LATCH -> 1
LATCH -> 0
LATCH -> 1
LATCH -> 0
LATCH -> 1
LATCH -> 0
LATCH -> 1
LATCH -> 0
LATCH -> 1
LATCH -> 0
LATCH -> 1
LATCH -> 0
LATCH -> 1
LATCH -> 0
LATCH -> 1
LATCH -> 0
LATCH -> 1
LATCH -> 0
LATCH -> 1
LATCH -> 0
LATCH -> 1
LATCH -> 0
LATCH -> 1
LATCH -> 0
LATCH -> 1
LATCH -> 0
LATCH -> 1
LATCH -> 0
LATCH -> 1
LATCH -> 0
'''