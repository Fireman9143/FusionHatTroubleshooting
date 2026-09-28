'''This is checking to see if extra clockings are being registered at pin 11'''


from fusion_hat.pin import Pin, Mode
import time

SRCLK = Pin(27, mode=Mode.OUT)

SRCLK.low()
time.sleep(2)

for i in range(8):
    print("CLOCK HIGH", i + 1)
    SRCLK.high()
    time.sleep(2)

    print("CLOCK LOW", i + 1)
    SRCLK.low()
    time.sleep(2)

SRCLK.low()
SRCLK.close()

print("Done")

'''
I left only D3 hooked up to arduino and accidentally ran the previous pi program getting this:
Waiting...
Edge 1: DATA=0 LATCH=0
Edge 2: DATA=0 LATCH=0
Edge 3: DATA=0 LATCH=0
Edge 4: DATA=0 LATCH=0
Edge 5: DATA=0 LATCH=0
Edge 6: DATA=0 LATCH=0
Edge 7: DATA=0 LATCH=0
Edge 8: DATA=0 LATCH=0
Edge 9: DATA=0 LATCH=0
Edge 10: DATA=0 LATCH=0
Edge 11: DATA=0 LATCH=0
Edge 12: DATA=0 LATCH=0
When I ran the current pi test, it did this:
Waiting...
Edge 1: DATA=0 LATCH=0
Edge 2: DATA=0 LATCH=0
Edge 3: DATA=0 LATCH=0
Edge 4: DATA=0 LATCH=0
Edge 5: DATA=0 LATCH=0
Edge 6: DATA=0 LATCH=0
Edge 7: DATA=0 LATCH=0
Edge 8: DATA=0 LATCH=0
'''