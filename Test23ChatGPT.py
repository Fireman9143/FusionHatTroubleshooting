'''This test is like test 22.  It is checking the RCLCK and DATA to see if bits are registering'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

SDI.high()

print("DS HIGH")
print("Clocking 8 times...")

for i in range(8):
    print("Clock", i + 1)

    SRCLK.low()
    time.sleep(0.5)

    SRCLK.high()
    time.sleep(0.5)

    SRCLK.low()
    time.sleep(0.5)

print("Finished.")
time.sleep(5)