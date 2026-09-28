'''Going back to testing Q0'''

from fusion_hat.pin import Pin, Mode
import time

SDI   = Pin(17, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)
RCLK  = Pin(4, mode=Mode.OUT)
DIGIT = Pin(23, mode=Mode.OUT)

# Disable digit
DIGIT.low()

# Send 11111110
for bit in [1, 1, 1, 1, 1, 1, 1, 0]:

    if bit:
        SDI.high()
    else:
        SDI.low()

    SRCLK.high()
    SRCLK.low()

RCLK.high()
RCLK.low()

# Turn on first digit
DIGIT.high()

print("Testing Q0 -> display A")
print("Leave this running for 10 seconds.")

time.sleep(10)