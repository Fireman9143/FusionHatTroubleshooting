'''This was the final test suggested by ChatGPT before Clause discovered that moving 
to pins 5, 6, and 13 resolved the issue'''

from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)

# Establish known idle states
SDI.low()
SRCLK.low()
RCLK.low()

time.sleep(1)

print("Sending eight ZERO bits...")

for i in range(8):
    print(f"Bit {i}: DATA LOW")

    SDI.low()
    time.sleep(0.5)

    print("       CLOCK HIGH")
    SRCLK.high()
    time.sleep(0.5)

    print("       CLOCK LOW")
    SRCLK.low()
    time.sleep(0.5)

print("LATCH")
RCLK.high()
time.sleep(0.5)
RCLK.low()

print("Done. Waiting 5 seconds.")
time.sleep(5)

SDI.low()
SRCLK.low()
RCLK.low()

SDI.close()
SRCLK.close()
RCLK.close()