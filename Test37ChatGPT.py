'''This test starts to move to different GPIO pins to check if it's a pin problem'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
SRCLK = Pin(22, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)

SDI.low()
SRCLK.low()
RCLK.low()

# Put a HIGH on DS
print("DS HIGH")
SDI.high()
time.sleep(2)

# One clock pulse
print("CLOCK HIGH")
SRCLK.high()
time.sleep(2)

print("CLOCK LOW")
SRCLK.low()
time.sleep(2)

# Latch
print("LATCH HIGH")
RCLK.high()
time.sleep(2)

print("LATCH LOW")
RCLK.low()
time.sleep(2)