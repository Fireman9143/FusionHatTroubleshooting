'''This goes back to testing the 595 and monitoring GPIO 17. Also using Arduino (78)'''

from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)

print("GPIO17 HIGH")
SDI.high()
time.sleep(5)

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
High showed 3.3v, low showed 0v
DATA changed -> 0 
DATA changed -> 0 
DATA changed -> 1 
DATA changed -> 0 
DATA changed -> 1 
DATA changed -> 0'''