'''This is now attempting to just get a 0 to display in digit 1'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

# Digit 1
DIG1 = Pin(23, mode=Mode.OUT)
DIG2 = Pin(24, mode=Mode.OUT)
DIG3 = Pin(25, mode=Mode.OUT)
DIG4 = Pin(12, mode=Mode.OUT)

digits = [DIG1, DIG2, DIG3, DIG4]

# Common-anode "0"
# A B C D E F = ON, G = OFF, DP = OFF
zero = 0xC0

# Turn ALL digits off
for pin in digits:
    pin.low()

# Shift 0xC0, MSB first
for i in range(8):
    bit = 1 if (zero & (0x80 >> i)) else 0
    SDI.value(bit)

    SRCLK.high()
    time.sleep(0.001)
    SRCLK.low()
    time.sleep(0.001)

# Latch
RCLK.high()
time.sleep(0.001)
RCLK.low()

# Turn on ONLY digit 1
DIG1.high()

print("Digit 1 selected.")
print("0xC0 latched.")
print("You should see a single 0 on the FIRST digit.")

time.sleep(10)

for pin in digits:
    pin.low()

SDI.close()
RCLK.close()
SRCLK.close()

for pin in digits:
    pin.close()