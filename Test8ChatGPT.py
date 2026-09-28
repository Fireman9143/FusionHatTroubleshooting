'''This is another attempt to isolate the 595 and measure the status of pin 15 on it'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

def shift(data):
    # Keep latch low while shifting
    RCLK.low()

    for i in range(8):
        if data & 0x80:
            SDI.high()
        else:
            SDI.low()

        SRCLK.low()
        time.sleep(0.05)

        SRCLK.high()       # shift on rising edge
        time.sleep(0.05)

        data <<= 1

    SRCLK.low()

    # Transfer shift register to output register
    RCLK.high()
    time.sleep(0.05)
    RCLK.low()


try:
    while True:
        print("Sending 0x00")
        shift(0x00)
        time.sleep(2)

        print("Sending 0x01")
        shift(0x01)
        time.sleep(2)

except KeyboardInterrupt:
    pass

finally:
    SDI.low()
    RCLK.low()
    SRCLK.low()

    SDI.close()
    RCLK.close()
    SRCLK.close()