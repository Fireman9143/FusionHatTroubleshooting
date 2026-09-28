'''Test 2 and associated tweaks produced lighted segments that had one segment blank out
each time through the rotation.  This code is another attempt to shift 0's through digits'''

from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

placePin = [Pin(pin, mode=Mode.OUT) for pin in (23, 24, 25, 12)]


def hc595_shift(data):
    for i in range(8):
        SDI.value(0x80 & (data << i))
        SRCLK.high()
        SRCLK.low()

    RCLK.high()
    RCLK.low()


try:
    while True:

        # Turn all digits OFF
        for pin in placePin:
            pin.low()

        # Send the pattern for ZERO
        hc595_shift(0xc0)

        # Display it on each position
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