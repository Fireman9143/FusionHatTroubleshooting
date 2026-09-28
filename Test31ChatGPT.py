'''This test went back to pin 12 to check it's ability to change state'''

from fusion_hat.pin import Pin, Mode
import time

RCLK = Pin(4, mode=Mode.OUT)

while True:
    RCLK.low()
    time.sleep(3)

    RCLK.high()
    time.sleep(3)