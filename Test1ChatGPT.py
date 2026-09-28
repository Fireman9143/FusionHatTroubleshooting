'''The first attempt to run Sunfounder example displayed "t.t.t.t." so this is ChatGPT's
first attempt to troubleshoot.  It should produce a 0 in each digit, one digit at a time'''

#!/usr/bin/env python3
from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

placePin = [Pin(pin, mode=Mode.OUT) for pin in (23, 24, 25, 12)]

number = (0xc0, 0xf9, 0xa4, 0xb0, 0x99,
          0x92, 0x82, 0xf8, 0x80, 0x90)

def hc595_shift(data):
    for i in range(8):
        SDI.value(1 if (data & (0x80 >> i)) else 0)
        SRCLK.high()
        SRCLK.low()

    RCLK.high()
    RCLK.low()

def clear_display():
    hc595_shift(0xff)

try:
    while True:
        for digit in range(4):
            # Turn all digits off
            for pin in placePin:
                pin.low()

            # Put a 0 on the shift register
            hc595_shift(number[0])

            # Turn on one digit
            placePin[digit].high()

            time.sleep(0.5)

finally:
    for pin in placePin:
        pin.low()

    clear_display()

    SDI.close()
    RCLK.close()
    SRCLK.close()

    for pin in placePin:
        pin.close()