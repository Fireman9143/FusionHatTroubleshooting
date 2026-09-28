'''Testing Q0 with 1's then 0's'''

from fusion_hat.pin import Pin, Mode
import time

SDI   = Pin(17, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)
RCLK  = Pin(4, mode=Mode.OUT)

def shift_byte(bits):
    for bit in bits:
        if bit:
            SDI.high()
        else:
            SDI.low()

        time.sleep(0.5)

        SRCLK.high()
        time.sleep(0.5)

        SRCLK.low()
        time.sleep(0.5)

    RCLK.high()
    time.sleep(0.5)
    RCLK.low()
    time.sleep(0.5)


SDI.low()
SRCLK.low()
RCLK.low()

print("Sending 00000000...")
shift_byte([0,0,0,0,0,0,0,0])

print("ZERO TEST - measure Q0 now")
time.sleep(10)

print("Sending 11111111...")
shift_byte([1,1,1,1,1,1,1,1])

print("ONE TEST - measure Q0 now")
time.sleep(10)

'''
During that test 595 pin 15 stayed high without changing.  
I also ran the arduino monitor and got this:
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
Edge 12: DATA=0 LATCH=0
Edge 13: DATA=0 LATCH=0
Edge 14: DATA=0 LATCH=0
Edge 15: DATA=0 LATCH=0
Edge 16: DATA=0 LATCH=0
'''