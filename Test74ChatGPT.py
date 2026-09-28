'''This test is to watch GPIO 17 with the arduino.  Matching arduino sketch will be 
Test74ChatGPTArduino'''

from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)

print("GPIO17 DATA TEST")
print("================")
print()

for i in range(5):

    print("GPIO17 -> HIGH")
    SDI.high()
    time.sleep(2)

    print("GPIO17 -> LOW")
    SDI.low()
    time.sleep(2)

print("Done.")

SDI.low()
SDI.close()

'''
DATA changed -> 1
DATA changed -> 1
'''