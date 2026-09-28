'''This is another test to alternate the state of pin 15 and measure it'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

def shift(data):
    RCLK.low()

    for _ in range(8):
        if data & 0x80:
            SDI.high()
        else:
            SDI.low()

        SRCLK.low()
        time.sleep(0.1)
        SRCLK.high()
        time.sleep(0.1)

        data <<= 1

    SRCLK.low()

    RCLK.high()
    time.sleep(0.2)
    RCLK.low()


try:
    while True:
        print("===== 0x00 =====")
        shift(0x00)
        time.sleep(3)

        print("===== 0xFF =====")
        shift(0xFF)
        time.sleep(3)

except KeyboardInterrupt:
    pass

finally:
    SDI.low()
    SRCLK.low()
    RCLK.low()

    SDI.close()
    SRCLK.close()
    RCLK.close()