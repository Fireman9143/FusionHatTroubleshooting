'''This is another attempt to test clocking from another GPIO pin'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
SRCLK = Pin(22, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)

SDI.low()
SRCLK.low()
RCLK.low()

print("Shifting 7 ZERO bits...")

for _ in range(7):
    SDI.low()
    SRCLK.high()
    time.sleep(0.2)
    SRCLK.low()
    time.sleep(0.2)

print("7 zeros shifted.")

print("Shifting final ONE bit...")

SDI.high()
SRCLK.high()
time.sleep(0.2)
SRCLK.low()
time.sleep(0.2)

print("All 8 bits shifted.")
time.sleep(2)

print("Latching...")
RCLK.high()
time.sleep(1)
RCLK.low()

print("Done.")
time.sleep(5)