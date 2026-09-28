'''This test goes back to test pin 12 to latch'''


from fusion_hat.pin import Pin, Mode
import time

RCLK = Pin(4, mode=Mode.OUT)

print("RCLK LOW")
RCLK.low()
time.sleep(5)

print("RCLK HIGH")
RCLK.high()
time.sleep(5)

print("RCLK LOW")
RCLK.low()
time.sleep(2)

RCLK.close()