'''Trying to just isolate pin 9 Q7' status changes'''

from fusion_hat.pin import Pin, Mode
from time import sleep

SDI = Pin(17, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

SDI.low()
SRCLK.low()

print("Clearing shift register is being done manually.")
print()
print("Set pin 10 HIGH.")
print("Pin 9 should currently be LOW.")
input("Press ENTER when ready...")

# Put ONE into the serial input
print()
print("DATA = HIGH")
SDI.high()

sleep(2)

print("Clock 1")
SRCLK.high()
sleep(2)
SRCLK.low()

print()
print("Measure pin 9 now.")
print("It may still be LOW because the 1 has only entered Q0.")
input("Press ENTER to continue...")

# Clock 2
print("Clock 2")
SRCLK.high()
sleep(2)
SRCLK.low()

input("Press ENTER...")

# Clock 3
print("Clock 3")
SRCLK.high()
sleep(2)
SRCLK.low()

input("Press ENTER...")

# Clock 4
print("Clock 4")
SRCLK.high()
sleep(2)
SRCLK.low()

input("Press ENTER...")

# Clock 5
print("Clock 5")
SRCLK.high()
sleep(2)
SRCLK.low()

input("Press ENTER...")

# Clock 6
print("Clock 6")
SRCLK.high()
sleep(2)
SRCLK.low()

input("Press ENTER...")

# Clock 7
print("Clock 7")
SRCLK.high()
sleep(2)
SRCLK.low()

input("Press ENTER...")

# Clock 8
print("Clock 8")
SRCLK.high()
sleep(2)
SRCLK.low()

print()
print("8 clocks complete.")
print("Measure pin 9.")
input("Press ENTER to finish...")