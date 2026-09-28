'''This was another attempt to shift bits and latch, measuring states before and after'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

SDI.low()
SRCLK.low()

print("Sending 8 HIGH bits...")

for i in range(8):
    SDI.high()
    time.sleep(0.2)

    SRCLK.high()
    time.sleep(0.2)

    SRCLK.low()
    time.sleep(0.2)

print("Done.")
print("Pin 15 should still be HIGH because pin 12 is HIGH.")
time.sleep(5)