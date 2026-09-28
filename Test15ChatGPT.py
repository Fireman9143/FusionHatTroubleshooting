'''This test is meant to only shift one bit and make pin 15 high'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

SDI.low()
RCLK.low()
SRCLK.low()

print("Shifting 00000001...")

for i in range(8):
    if i == 7:
        SDI.high()
    else:
        SDI.low()

    SRCLK.high()
    time.sleep(0.1)
    SRCLK.low()
    time.sleep(0.1)

print("Latching...")

RCLK.high()
time.sleep(0.2)
RCLK.low()

print("Q0 should now be HIGH.")
print("Measure pin 15.")

time.sleep(10)

SDI.low()
SRCLK.low()
RCLK.low()

SDI.close()
SRCLK.close()
RCLK.close()