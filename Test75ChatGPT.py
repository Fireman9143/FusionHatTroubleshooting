'''This test plugged GPIO 17 straight into the ardiuno for monitoring.'''

from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)

print("GPIO17 LOW")
SDI.low()
time.sleep(5)

print("GPIO17 HIGH")
SDI.high()
time.sleep(5)

print("GPIO17 LOW")
SDI.low()
time.sleep(5)

SDI.close()

'''
DATA changed 
DATA changed -> 0 
DATA changed -> 1
'''