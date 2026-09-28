'''After rechecking wiring, this is another test slowed down to check latching'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)
DIG1 = Pin(23, mode=Mode.OUT)

# Everything off initially
DIG1.low()
SDI.low()
SRCLK.low()
RCLK.low()

print("Starting very slow 0x00 test.")
print()
print("Watch the meter on 595 pin 15.")
print()

# Send eight ZERO bits, one at a time
for i in range(8):
    print(f"Bit {i}: DATA = LOW")

    SDI.low()
    time.sleep(2)

    print("  CLOCK HIGH")
    SRCLK.high()
    time.sleep(2)

    print("  CLOCK LOW")
    SRCLK.low()
    time.sleep(2)

print()
print("All eight zeroes have been shifted.")
print("Pin 15 is still the OLD output until we latch.")
time.sleep(3)

print()
print("LATCH HIGH")
RCLK.high()
time.sleep(2)

print("LATCH LOW")
RCLK.low()
time.sleep(5)

print()
print("Now enabling digit 1.")
DIG1.high()

time.sleep(10)

DIG1.low()

SDI.close()
RCLK.close()
SRCLK.close()
DIG1.close()