'''This test was sending deliberate patterns and checking for the pin response'''

from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

SDI.low()
SRCLK.low()

bits = [1, 0, 1, 0, 1, 0, 1, 0]

print()
print("SHIFT REGISTER TEST")
print("====================")
print("Pattern being shifted: 10101010")
print()
print("Measure 595 pin 9 (Q7') after each CLOCK LOW.")
print()

for i, bit in enumerate(bits):

    print(f"\nBit {i+1} of 8")
    print(f"DATA = {bit}")

    SDI.value(bit)
    time.sleep(1)

    print("CLOCK HIGH")
    SRCLK.high()
    time.sleep(1)

    print("CLOCK LOW")
    SRCLK.low()
    time.sleep(1)

    print(">>> Measure 595 pin 9 (Q7')")
    result = input("Enter H or L: ").strip().upper()

    print(f"You recorded: {result}")

print()
print("Test complete.")

SDI.low()
SRCLK.low()

SDI.close()
SRCLK.close()

'''
SHIFT REGISTER TEST
====================
Pattern being shifted: 10101010

Measure 595 pin 9 (Q7') after each CLOCK LOW.


Bit 1 of 8
DATA = 1
CLOCK HIGH
CLOCK LOW
>>> Measure 595 pin 9 (Q7')
Enter H or L: h
You recorded: H

Bit 2 of 8
DATA = 0
CLOCK HIGH
CLOCK LOW
>>> Measure 595 pin 9 (Q7')
Enter H or L: h
You recorded: H

Bit 3 of 8
DATA = 1
CLOCK HIGH
CLOCK LOW
>>> Measure 595 pin 9 (Q7')
Enter H or L: h
You recorded: H

Bit 4 of 8
DATA = 0
CLOCK HIGH
CLOCK LOW
>>> Measure 595 pin 9 (Q7')
Enter H or L: l
You recorded: L

Bit 5 of 8
DATA = 1
CLOCK HIGH
CLOCK LOW
>>> Measure 595 pin 9 (Q7')
Enter H or L: h
You recorded: H

Bit 6 of 8
DATA = 0
CLOCK HIGH
CLOCK LOW
>>> Measure 595 pin 9 (Q7')
Enter H or L: h
You recorded: H

Bit 7 of 8
DATA = 1
CLOCK HIGH
CLOCK LOW
>>> Measure 595 pin 9 (Q7')
Enter H or L: l
You recorded: L

Bit 8 of 8
DATA = 0
CLOCK HIGH
CLOCK LOW
>>> Measure 595 pin 9 (Q7')
Enter H or L: l
You recorded: L

Test complete.'''