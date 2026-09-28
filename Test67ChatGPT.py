'''Now were starting to use Q7' to see the previous latched state'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

SDI.low()
SRCLK.low()
RCLK.low()

print("Starting...")
print()
print("We will shift ONE ZERO followed by SEVEN ONES.")
print("Measure 595 pin 9 (Q7') after each clock.")
print()

# 0 1 1 1 1 1 1 1
bits = [0, 1, 1, 1, 1, 1, 1, 1]

for i, bit in enumerate(bits):

    SDI.value(bit)

    print(f"Bit {i}: DATA = {bit}")
    print("  Data is set. Measure pin 14 if desired.")
    time.sleep(2)

    print("  CLOCK HIGH")
    SRCLK.high()
    time.sleep(2)

    print("  CLOCK LOW")
    SRCLK.low()
    time.sleep(2)

    print("  Measure pin 9 (Q7')")
    input("  Press ENTER to continue...")

print()
print("Done.")

SDI.low()
SRCLK.low()
RCLK.low()

SDI.close()
RCLK.close()
SRCLK.close()