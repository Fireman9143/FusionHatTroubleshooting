'''Because of the random segment lighting, this test was meant to turn on and check each segment
in the first digit'''


#!/usr/bin/env python3

from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

placePin = [Pin(pin, mode=Mode.OUT) for pin in (23, 24, 25, 12)]


def hc595_shift(data):
    for i in range(8):
        if data & 0x80:
            SDI.high()
        else:
            SDI.low()

        SRCLK.high()
        SRCLK.low()

        data <<= 1

    RCLK.high()
    RCLK.low()


try:

    # Use only the first display position
    for pin in placePin:
        pin.low()

    placePin[0].high()

    # Each value turns ON exactly ONE segment.
    # The display is active-low.
    patterns = [
        0x7f,   # Q7 = 0
        0xbf,   # Q6 = 0
        0xdf,   # Q5 = 0
        0xef,   # Q4 = 0
        0xf7,   # Q3 = 0
        0xfb,   # Q2 = 0
        0xfd,   # Q1 = 0
        0xfe,   # Q0 = 0
    ]

    for pattern in patterns:

        hc595_shift(pattern)

        print(f"Pattern: 0x{pattern:02X}")

        time.sleep(2)

finally:

    for pin in placePin:
        pin.low()

    hc595_shift(0xff)

    SDI.close()
    RCLK.close()
    SRCLK.close()

    for pin in placePin:
        pin.close()