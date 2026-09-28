'''This is another test to see if Q0 is functioning correctly'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

SDI.low()
SRCLK.low()
RCLK.low()

# Shift eight zeroes
for i in range(8):
    SDI.low()
    SRCLK.high()
    time.sleep(0.01)
    SRCLK.low()
    time.sleep(0.01)

# Latch
RCLK.high()
time.sleep(0.01)
RCLK.low()

print("0x00 loaded. Q0-Q7 should all be LOW.")
print("Measure 595 pin 15 (Q0) now.")
time.sleep(10)

SDI.close()
RCLK.close()
SRCLK.close()