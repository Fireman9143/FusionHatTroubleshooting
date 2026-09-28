'''This is another attempt to shift bits, latch, and measure pin 15'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

SDI.low()
SRCLK.low()

# Shift eight 1s into the 595
for i in range(8):
    SDI.high()
    SRCLK.high()
    time.sleep(0.2)
    SRCLK.low()
    time.sleep(0.2)

print("Eight 1s shifted.")
print("Pin 15 should still be LOW.")
time.sleep(3)