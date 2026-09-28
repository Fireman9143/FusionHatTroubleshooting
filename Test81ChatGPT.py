'''Again measuring Q0-Q7, this time also monitoring with arduino'''

from fusion_hat.pin import Pin, Mode
import time

SDI   = Pin(17, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)
RCLK  = Pin(4, mode=Mode.OUT)

# Start everything LOW
SDI.low()
SRCLK.low()
RCLK.low()

time.sleep(2)

# 0xAA = 10101010
bits = [1, 0, 1, 0, 1, 0, 1, 0]

print("Shifting 10101010")

for bit in bits:

    if bit:
        SDI.high()
    else:
        SDI.low()

    # Give the DATA signal plenty of time to settle
    time.sleep(1)

    SRCLK.high()
    time.sleep(1)

    SRCLK.low()
    time.sleep(1)

print("Finished shifting.")
print("Now latching...")

RCLK.high()
time.sleep(1)

RCLK.low()
time.sleep(1)

print("Latched.")

# Leave the shift-register inputs LOW,
# but don't change the latch/output state.
SDI.low()
SRCLK.low()

time.sleep(5)

SDI.close()
SRCLK.close()
RCLK.close()

'''
That alternated 3.3v and 0v from Q0 to Q7 as expected.  
I also kept the serial window open and got this from the arduino:
Waiting...
Edge 1: DATA=1 LATCH=0
Edge 2: DATA=1 LATCH=0
Edge 3: DATA=1 LATCH=0
Edge 4: DATA=1 LATCH=0
Edge 5: DATA=1 LATCH=0
Edge 6: DATA=1 LATCH=0
Edge 7: DATA=1 LATCH=0
Edge 8: DATA=1 LATCH=0
Edge 9: DATA=1 LATCH=0
Edge 10: DATA=1 LATCH=0
Edge 11: DATA=1 LATCH=0
Edge 12: DATA=1 LATCH=0
Edge 13: DATA=1 LATCH=0
Edge 14: DATA=1 LATCH=0
Edge 15: DATA=1 LATCH=0
Edge 16: DATA=1 LATCH=0
'''