'''Going back to testing just Q0 to be low'''

from fusion_hat.pin import Pin, Mode
import time

SDI   = Pin(17, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)
RCLK  = Pin(4, mode=Mode.OUT)

SDI.low()
SRCLK.low()
RCLK.low()

print("Sending 00000000")

for i in range(8):
    SRCLK.high()
    time.sleep(0.2)
    SRCLK.low()
    time.sleep(0.2)

RCLK.high()
time.sleep(0.2)
RCLK.low()

print("Done - measure Q0 (595 pin 15)")
time.sleep(10)