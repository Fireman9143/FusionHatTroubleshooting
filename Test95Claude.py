#!/usr/bin/env python3
from fusion_hat.pin import Pin, Mode
import time

print("Creating pin objects...")
SDI = Pin(17, mode=Mode.OUT)      # Serial Data Input
RCLK = Pin(4, mode=Mode.OUT)      # Register Clock
SRCLK = Pin(27, mode=Mode.OUT)    # Shift Register Clock
MEMCLEAR = Pin(26, mode=Mode.OUT) # Low to clear 595 shift register (MR/SRCLR)

placePin = [Pin(pin, mode=Mode.OUT) for pin in (23, 24, 25, 12)]
print("Pin objects created successfully.")

# Segment codes for 0-9, matching your confirmed SunFounder pinout
# (Q0=b, Q1=c, Q2=d, Q3=e, Q4=f, Q5=g, Q6=DP, Q7=a)
number = (0x60, 0xfc, 0x52, 0x58, 0xcc, 0x49, 0x41, 0x7c, 0x40, 0x48)


def clearDisplay():
    for _ in range(8):
        SDI.high()
        SRCLK.high()
        SRCLK.low()
    RCLK.high()
    RCLK.low()


def hc595_shift(data):
    for i in range(8):
        SDI.value(1 if (data & (0x80 >> i)) else 0)
        SRCLK.high()
        SRCLK.low()
    RCLK.high()
    RCLK.low()


def pickDigit(digit):
    for pin in placePin:
        pin.low()
    placePin[digit].high()


def show_number_on_all_digits(n, duration=1.0):
    """Multiplex the same digit n (0-9) onto all four display positions for `duration` seconds."""
    end_time = time.time() + duration
    while time.time() < end_time:
        for i in range(4):
            clearDisplay()
            pickDigit(i)
            hc595_shift(number[n])
            time.sleep(0.001)


try:
    print("Pulsing MEMCLEAR (595 master reset)...")
    MEMCLEAR.low()
    time.sleep(0.001)
    MEMCLEAR.high()
    print("MEMCLEAR pulse complete.")

    print("Entering main loop. Press Ctrl+C to stop.")
    while True:
        for n in range(10):
            print(f"Showing digit: {n}")
            show_number_on_all_digits(n, duration=1.0)

except KeyboardInterrupt:
    print("\nStopped by user (Ctrl+C).")

except Exception as e:
    print(f"\n*** ERROR: {type(e).__name__}: {e} ***")

finally:
    print("Cleaning up GPIO...")
    for device in [SDI, RCLK, SRCLK, MEMCLEAR] + placePin:
        try:
            device.close()
        except Exception:
            pass
    print("Done.")
