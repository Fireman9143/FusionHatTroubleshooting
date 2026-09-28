'''This is another attempt to display a 0 in the first digit'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

# Your actual digit wiring
DIG1 = Pin(22, mode=Mode.OUT)
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

# 0xC0 = common-anode "0"
hc595_shift(0xC0)

# Turn ON first digit
DIG1.high()

print("First digit should show 0.")
time.sleep(10)

DIG1.low()

SDI.close()
RCLK.close()
SRCLK.close()
DIG1.close()
DIG2.close()
DIG3.close()
DIG4.close()