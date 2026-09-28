'''A change now to check rising clock edges'''

from fusion_hat.pin import Pin, Mode
import time

SDI   = Pin(17, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)
RCLK  = Pin(4, mode=Mode.OUT)

SDI.low()
SRCLK.low()
RCLK.low()

time.sleep(2)

bits = [1, 0, 1, 0, 1, 0, 1, 0]

for bit in bits:

    print("DATA =", bit)

    if bit:
        SDI.high()
    else:
        SDI.low()

    time.sleep(1)

    print("CLOCK HIGH")
    SRCLK.high()
    time.sleep(1)

    print("CLOCK LOW")
    SRCLK.low()
    time.sleep(1)

print("LATCH HIGH")
RCLK.high()
time.sleep(1)

print("LATCH LOW")
RCLK.low()
time.sleep(1)

SDI.low()
SRCLK.low()
RCLK.low()

SDI.close()
SRCLK.close()
RCLK.close()

'''
Edge 1: DATA=1 LATCH=0
Edge 2: DATA=0 LATCH=0
Edge 3: DATA=1 LATCH=0
Edge 4: DATA=1 LATCH=0
Edge 5: DATA=0 LATCH=0
Edge 6: DATA=1 LATCH=0
Edge 7: DATA=0 LATCH=0
Edge 8: DATA=1 LATCH=0
Edge 9: DATA=0 LATCH=0
Edge 10: DATA=0 LATCH=1
'''