'''This test is just to see if RCLCK is changing state correctly'''


from fusion_hat.pin import Pin, Mode
import time

RCLK = Pin(4, mode=Mode.OUT)

print("LOW")
RCLK.low()
time.sleep(5)

print("HIGH")
RCLK.high()
time.sleep(5)

print("LOW")
RCLK.low()
time.sleep(5)

RCLK.close()