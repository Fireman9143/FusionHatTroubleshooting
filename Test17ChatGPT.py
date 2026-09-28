'''This is another attempt to alternate the state of pin 15 and measure with DMM'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

def shift(data):
    RCLK.low()

    for _ in range(8):
        SDI.value(1 if data & 0x80 else 0)

        SRCLK.low()
        time.sleep(0.05)
        SRCLK.high()
        time.sleep(0.05)

        data <<= 1

    SRCLK.low()

    RCLK.high()
    time.sleep(0.1)
    RCLK.low()

try:
    print("Sending 0x00")
    shift(0x00)
    time.sleep(3)

    print("Sending 0xFF")
    shift(0xFF)
    time.sleep(3)

    print("Sending 0x00")
    shift(0x00)
    time.sleep(3)

finally:
    SDI.low()
    SRCLK.low()
    RCLK.low()

    SDI.close()
    SRCLK.close()
    RCLK.close()