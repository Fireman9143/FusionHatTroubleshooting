'''This test goes back to test just data on pin 14'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)

print("SDI LOW")
SDI.low()
time.sleep(5)

print("SDI HIGH")
SDI.high()
time.sleep(5)

SDI.low()
SDI.close()