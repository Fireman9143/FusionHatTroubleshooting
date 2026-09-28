'''The first test resulted in "t." going from one digit to the next.  This is a slightly changed
code to try to get a 0 to light in each digit, one digit at a time'''

from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

placePin = [Pin(pin, mode=Mode.OUT) for pin in (23, 24, 25, 12)]


def hc595_shift(data):
    for i in range(8):
        SDI.value(data & 0x80)
        data <<= 1

        SRCLK.high()
        SRCLK.low()

    RCLK.high()
    RCLK.low()


try:
    while True:

        # Turn all digits off
        for pin in placePin:
            pin.low()

        # Send the segment pattern for ZERO
        hc595_shift(0xc0)

        # Turn on each digit one at a time
        for i in range(4):
            placePin[i].high()
            time.sleep(1)
            placePin[i].low()

finally:
    for pin in placePin:
        pin.low()

    SDI.close()
    RCLK.close()
    SRCLK.close()

    for pin in placePin:
        pin.close()