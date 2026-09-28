'''This test is just to test the data pin to see if it changes state correctly'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)

print("LOW")
SDI.low()
time.sleep(5)

print("HIGH")
SDI.high()
time.sleep(5)

print("LOW")
SDI.low()
time.sleep(5)

SDI.close()