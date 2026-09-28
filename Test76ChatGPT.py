'''This test was checking .value() vs .low()/.high() with the same arduino sketch (74)
and GPIO 17 plugged straight to arduino'''

from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)

print("Testing SDI.value()")

for i in range(5):
    print("value(1)")
    SDI.value(1)
    time.sleep(2)

    print("value(0)")
    SDI.value(0)
    time.sleep(2)

SDI.low()
SDI.close()

print("Done")

'''
DATA changed -> 1
'''