'''This test is going back to measure Q0 and compare to the display pin to be sure the problem
isn't in a bad connection'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)
DIG1 = Pin(23, mode=Mode.OUT)

# Turn digit 1 OFF while we load the data
DIG1.low()

# Shift 0xFE:
# Q0 should end LOW
for i in range(8):
    bit = 1 if (0xFE & (0x80 >> i)) else 0
    SDI.value(bit)
    SRCLK.high()
    SRCLK.low()

# Latch
RCLK.high()
RCLK.low()

print("0xFE loaded.")
print("Now turn digit 1 on.")

DIG1.high()

time.sleep(5)

DIG1.low()

SDI.close()
RCLK.close()
SRCLK.close()
DIG1.close()