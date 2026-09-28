'''This test is just to test SRCLK to see if it changes state correctly'''


from fusion_hat.pin import Pin, Mode
import time

SRCLK = Pin(27, mode=Mode.OUT)

print("LOW")
SRCLK.low()
time.sleep(5)

print("HIGH")
SRCLK.high()
time.sleep(5)

print("LOW")
SRCLK.low()
time.sleep(5)

SRCLK.close()