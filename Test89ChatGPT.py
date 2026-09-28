'''New test looking at Q7' and monitoring with arduino.  At some point I had put LEDs
on Q0-Q7 to monitor their high/low status'''


from fusion_hat.pin import Pin, Mode
from time import sleep

SDI = Pin(17, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)

SDI.low()
SRCLK.low()
RCLK.low()

print()
print("================================")
print("Q7' SHIFT TEST")
print("================================")
print()
print("Sending: 10101010")
print()

bits = [1, 0, 1, 0, 1, 0, 1, 0]

for i, bit in enumerate(bits):

    if bit:
        SDI.high()
    else:
        SDI.low()

    sleep(1)

    print(f"Clock {i + 1}: DATA={bit}")

    SRCLK.high()
    sleep(1)

    SRCLK.low()
    sleep(1)

print()
print("8 clocks complete.")
print()
print("Now latching...")

RCLK.high()
sleep(1)
RCLK.low()

print()
print("DONE")
print("Waiting 10 seconds...")
sleep(10)

'''
all leds stayed on

==============================
=================================
  595 Q7' SHIFT REGISTER TEST
=================================

D3 = CLOCK
D5 = Q7'

Waiting...
CLOCK 1   Q7'=1
CLOCK 2   Q7'=1
CLOCK 3   Q7'=1
CLOCK 4   Q7'=1
CLOCK 5   Q7'=1
CLOCK 6   Q7'=1
CLOCK 7   Q7'=1
CLOCK 8   Q7'=1
CLOCK 9   Q7'=1
'''