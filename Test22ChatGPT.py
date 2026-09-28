'''This is to check pin 11 and 14 to see if bits are registering.'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

# Put a HIGH on the data input
SDI.high()

print("DS (pin 14) = HIGH")
print("Clocking 8 times...")

for i in range(8):
    print("Clock", i + 1)

    SRCLK.low()
    time.sleep(0.5)

    SRCLK.high()
    time.sleep(0.5)

    SRCLK.low()
    time.sleep(0.5)

print("Finished. Q0 should NOT necessarily change yet.")
time.sleep(5)