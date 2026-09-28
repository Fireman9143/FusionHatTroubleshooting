'''This test is designed to change only the status of pin 15 on the 74HC595.  The output was
measured with a DMM'''


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
        time.sleep(0.01)
        SRCLK.high()
        time.sleep(0.01)

        data <<= 1

    SRCLK.low()

    RCLK.high()
    time.sleep(0.01)
    RCLK.low()


try:
    while True:
        # 00000000
        shift(0x00)
        print("0x00")
        time.sleep(2)

        # 10000000
        shift(0x80)
        print("0x80")
        time.sleep(2)

finally:
    SDI.low()
    RCLK.low()
    SRCLK.low()

    SDI.close()
    RCLK.close()
    SRCLK.close()