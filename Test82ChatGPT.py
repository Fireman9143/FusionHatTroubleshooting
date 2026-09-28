'''Attempting to light individual segment in digit 1'''

from fusion_hat.pin import Pin, Mode
import time

SDI   = Pin(17, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)
RCLK  = Pin(4, mode=Mode.OUT)

DIGIT1 = Pin(23, mode=Mode.OUT)

# Disable all digits initially
DIGIT1.low()

SDI.low()
SRCLK.low()
RCLK.low()

# Send 11111110
# Q0 = 0
# Q1-Q7 = 1

bits = [1, 1, 1, 1, 1, 1, 1, 0]

for bit in bits:
    if bit:
        SDI.high()
    else:
        SDI.low()

    time.sleep(0.1)

    SRCLK.high()
    time.sleep(0.1)

    SRCLK.low()
    time.sleep(0.1)

# Latch
RCLK.high()
time.sleep(0.1)
RCLK.low()

# Enable digit 1
DIGIT1.high()

print("Digit 1 / segment A should be ON.")

time.sleep(10)

DIGIT1.low()

SDI.low()
SRCLK.low()
RCLK.low()

DIGIT1.close()
SDI.close()
SRCLK.close()
RCLK.close()