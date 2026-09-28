'''This is another test to see if bit changes are being stored at Q7'.'''

from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

SDI.low()
SRCLK.low()

print("Starting 8 ZERO bits")
print("Measure 595 pin 9 (Q7') after each clock.")
print()

for i in range(8):
    print(f"Bit {i}: DATA LOW")
    SDI.low()
    time.sleep(1)

    print("CLOCK HIGH")
    SRCLK.high()
    time.sleep(1)

    print("CLOCK LOW")
    SRCLK.low()
    time.sleep(1)

    print("Measure pin 9 now.")
    input("Press ENTER...")

print("Done.")

SDI.low()
SRCLK.low()

SDI.close()
SRCLK.close()