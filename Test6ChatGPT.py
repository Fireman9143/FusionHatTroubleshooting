'''This test was an attempt to light sequential numbers in the first digit only.  This was after
verifying the exact model of shift register and display.'''


#!/usr/bin/env python3

from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

# Keep all four digits OFF initially
placePin = [Pin(pin, mode=Mode.OUT) for pin in (23, 24, 25, 12)]

def shift_byte(data):
    # Make sure latch is LOW while shifting
    RCLK.low()

    for i in range(8):
        if data & 0x80:
            SDI.high()
        else:
            SDI.low()

        SRCLK.low()
        SRCLK.high()
        data <<= 1

    # Latch the result
    SRCLK.low()
    RCLK.high()
    time.sleep(0.1)
    RCLK.low()


try:
    # Select ONLY the first digit
    for pin in placePin:
        pin.low()

    placePin[0].high()

    while True:
        print("Sending 0xC0")
        shift_byte(0xC0)
        time.sleep(2)

        print("Sending 0xF9")
        shift_byte(0xF9)
        time.sleep(2)

        print("Sending 0xA4")
        shift_byte(0xA4)
        time.sleep(2)

        print("Sending 0xB0")
        shift_byte(0xB0)
        time.sleep(2)

finally:
    for pin in placePin:
        pin.low()

    shift_byte(0xFF)

    SDI.close()
    RCLK.close()
    SRCLK.close()

    for pin in placePin:
        pin.close()