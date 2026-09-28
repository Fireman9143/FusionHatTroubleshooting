'''This is another attempt to deliberately shift bits and measure pin 15'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

def shift(data):
    RCLK.low()

    for i in range(8):
        if data & 0x80:
            SDI.high()
        else:
            SDI.low()

        SRCLK.low()
        time.sleep(0.05)
        SRCLK.high()
        time.sleep(0.05)

        data <<= 1

    SRCLK.low()

    RCLK.high()
    time.sleep(0.1)
    RCLK.low()

print("Sending 0xFF")
shift(0xFF)

print("Measure pin 15 now.")
time.sleep(10)

SDI.low()
SRCLK.low()
RCLK.low()

SDI.close()
SRCLK.close()
RCLK.close()