'''This was similar to test 19, changing states and checking clocks, but with more time to measure'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

SDI.low()
SRCLK.low()
RCLK.low()

print("Shifting eight zeros...")

for i in range(8):
    SRCLK.high()
    time.sleep(0.25)
    SRCLK.low()
    time.sleep(0.25)

print("Eight zeros shifted.")
print("Latching now...")

RCLK.high()
time.sleep(1)
RCLK.low()

print("LATCH COMPLETE")
print("Pin 15 should now be LOW.")
print("Leaving GPIOs active for 30 seconds.")

time.sleep(30)