'''This was a test to deliberately measure high on pin 15'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

def shift(data):
    for _ in range(8):
        SDI.value(1 if data & 0x80 else 0)

        SRCLK.low()
        SRCLK.high()

        data <<= 1

    SRCLK.low()

    RCLK.low()
    RCLK.high()
    RCLK.low()

shift(0x01)

print("Sent 0x01 - measure pin 15")
time.sleep(10)

SDI.close()
RCLK.close()
SRCLK.close()