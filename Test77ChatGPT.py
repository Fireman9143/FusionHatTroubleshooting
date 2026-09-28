'''This is another test going back to .low()/.high() for pin control with arduino (74)'''

from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)

for i in range(5):
    print("HIGH")
    SDI.high()
    time.sleep(2)

    print("LOW")
    SDI.low()
    time.sleep(2)

SDI.low()
SDI.close()


'''
DATA changed -> 1
'''