'''This test is checking the clock, data, and latch each changing state as it should'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)

SDI.low()
SRCLK.low()
RCLK.low()

print("DS LOW")
time.sleep(2)

print("DS HIGH")
SDI.high()
time.sleep(2)

print("CLOCK HIGH")
SRCLK.high()
time.sleep(2)

print("CLOCK LOW")
SRCLK.low()
time.sleep(2)

print("LATCH HIGH")
RCLK.high()
time.sleep(2)

print("LATCH LOW")
RCLK.low()
time.sleep(2)