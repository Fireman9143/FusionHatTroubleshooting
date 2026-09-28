'''This is another test to check pin 15 after shifting bits and latching'''

from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)

SDI.low()
SRCLK.low()
RCLK.low()

print("Shifting 11111111")

for i in range(8):
    SDI.high()

    SRCLK.high()
    time.sleep(0.2)

    SRCLK.low()
    time.sleep(0.2)

print("Bits shifted. Q0 should STILL be LOW.")
time.sleep(2)

print("Latching...")

RCLK.high()
time.sleep(2)

RCLK.low()

print("Q0 should now be HIGH.")
time.sleep(5)