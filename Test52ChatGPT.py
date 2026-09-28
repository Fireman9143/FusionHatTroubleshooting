'''This code is an attempt to map the wiring from Q0-Q7 and the display segment pins'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)
DIG1 = Pin(23, mode=Mode.OUT)
DIG2 = Pin(24, mode=Mode.OUT)
DIG3 = Pin(25, mode=Mode.OUT)
DIG4 = Pin(12, mode=Mode.OUT)

def hc595_shift(data):
    for i in range(8):
        SDI.value(1 if (data & (0x80 >> i)) else 0)
        SRCLK.high()
        SRCLK.low()

    RCLK.high()
    RCLK.low()

# Turn all digits off
DIG1.low()
DIG2.low()
DIG3.low()
DIG4.low()

# Test each individual 595 bit
tests = [
    0x01,
    0x02,
    0x04,
    0x08,
    0x10,
    0x20,
    0x40,
    0x80,
]

for value in tests:
    hc595_shift(value)

    DIG1.high()

    print(f"Testing 0x{value:02X} - observe first digit")
    time.sleep(2)

    DIG1.low()
    time.sleep(0.5)

# Clear
hc595_shift(0xFF)

SDI.close()
RCLK.close()
SRCLK.close()
DIG1.close()
DIG2.close()
DIG3.close()
DIG4.close()