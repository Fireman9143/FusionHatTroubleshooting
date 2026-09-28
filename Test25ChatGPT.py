'''This test is now watching pin 12 to see if the chip latches'''


from fusion_hat.pin import Pin, Mode
import time

RCLK = Pin(4, mode=Mode.OUT)

while True:
    print("RCLK LOW")
    RCLK.low()
    time.sleep(3)

    print("RCLK HIGH")
    RCLK.high()
    time.sleep(3)