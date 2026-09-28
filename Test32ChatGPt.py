'''This is another test to see if clocking is working inside the chip'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)

# Everything LOW initially
SDI.low()
SRCLK.low()
RCLK.low()

print("1. Shifting eight 1s...")
for i in range(8):
    SDI.high()
    SRCLK.high()
    time.sleep(0.2)
    SRCLK.low()
    time.sleep(0.2)

print("2. Shift complete.")
print("Q0 should still be LOW.")
time.sleep(3)

print("3. RCLK HIGH")
RCLK.high()

print("Q0 should now be HIGH.")
time.sleep(5)

print("4. RCLK LOW")
RCLK.low()

time.sleep(3)