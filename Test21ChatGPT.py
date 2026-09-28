'''This test is to specifically watch the data pin'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)

SDI.low()
print("GPIO17 LOW")
time.sleep(3)

SDI.high()
print("GPIO17 HIGH")
time.sleep(3)

SDI.low()
print("GPIO17 LOW")
time.sleep(3)

SDI.close()