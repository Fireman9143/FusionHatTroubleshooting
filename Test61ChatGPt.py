'''This test goes back to check pin 11 to clock'''


from fusion_hat.pin import Pin, Mode
import time

SRCLK = Pin(27, mode=Mode.OUT)

print("SRCLK LOW")
SRCLK.low()
time.sleep(5)

print("SRCLK HIGH")
SRCLK.high()
time.sleep(5)

print("SRCLK LOW")
SRCLK.low()
time.sleep(2)

SRCLK.close()