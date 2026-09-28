'''Test three ultimately resulted in a blank display no matter what.  We now know this is 
because the memory was not being cleared.  Power cycling the Pi results in more random lit
segments that got fewer each cycle.  This is another attempt to identify what segments are
getting commands to turn on or off'''


#!/usr/bin/env python3

from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

placePin = [Pin(pin, mode=Mode.OUT) for pin in (23, 24, 25, 12)]

# Active-low segment codes
number = (
    0xc0,  # 0
    0xf9,  # 1
    0xa4,  # 2
    0xb0,  # 3
    0x99,  # 4
    0x92,  # 5
    0x82,  # 6
    0xf8,  # 7
    0x80,  # 8
    0x90   # 9
)


def hc595_shift(data):
    """Send one byte to the 74HC595, MSB first."""

    for i in range(8):
        bit = data & 0x80

        if bit:
            SDI.high()
        else:
            SDI.low()

        SRCLK.high()
        SRCLK.low()

        data <<= 1

    # Latch the shifted data onto Q0-Q7
    RCLK.high()
    RCLK.low()


def all_digits_off():
    for pin in placePin:
        pin.low()


try:

    all_digits_off()

    while True:

        for digit in range(4):

            # Make sure previous digit is off
            all_digits_off()

            # Send "0"
            hc595_shift(0xc0)

            # Select this digit
            placePin[digit].high()

            time.sleep(1)

finally:

    all_digits_off()

    # Turn segments off
    hc595_shift(0xff)

    SDI.low()
    SRCLK.low()
    RCLK.low()

    SDI.close()
    RCLK.close()
    SRCLK.close()

    for pin in placePin:
        pin.close()