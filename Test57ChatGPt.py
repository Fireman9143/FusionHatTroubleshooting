'''This is another test to check pin 15 is 3.3v'''

from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

SDI.low()
SRCLK.low()
RCLK.low()

# Shift 8 ones
for _ in range(8):
    SDI.high()
    SRCLK.high()
    time.sleep(0.05)
    SRCLK.low()
    time.sleep(0.05)

RCLK.high()
time.sleep(0.05)
RCLK.low()

print("0xFF loaded.")
print("Measure DIRECTLY on 595 pin 15.")
time.sleep(10)

SDI.close()
RCLK.close()
SRCLK.close()