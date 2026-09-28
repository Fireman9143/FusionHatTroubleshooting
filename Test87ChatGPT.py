'''New indepth testing with new arduino sketch (87)'''

from fusion_hat.pin import Pin, Mode
from time import sleep

SDI = Pin(17, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)


def clock():
    SRCLK.high()
    sleep(0.2)
    SRCLK.low()
    sleep(0.2)


def latch():
    RCLK.high()
    sleep(0.5)
    RCLK.low()
    sleep(0.5)


def shift_bit(bit):
    if bit:
        SDI.high()
    else:
        SDI.low()

    sleep(0.5)

    clock()


print()
print("================================")
print("595 SHIFT/LATCH TEST")
print("================================")
print()

# --------------------------------
# STEP 1
# Force DATA HIGH
# --------------------------------

print("STEP 1: DATA HIGH")
print("Shifting 8 ONES")
print()

SDI.high()

for i in range(8):
    print(f"Clock {i + 1}: DATA=1")
    clock()

print()
print("Latching ONES...")
latch()

print()
print("LEDs should now ALL be ON.")
print("Waiting 10 seconds...")
sleep(10)


# --------------------------------
# STEP 2
# Shift zeroes WITHOUT LATCH
# --------------------------------

print()
print("STEP 2: SHIFT ZEROES WITHOUT LATCH")
print()
print("The shift register will receive 8 zeroes.")
print("The LEDs should NOT change yet.")
print()

for i in range(8):
    print(f"Clock {i + 1}: DATA=0")
    shift_bit(0)

print()
print("8 zeroes shifted.")
print()
print("IMPORTANT:")
print("The LEDs should STILL all be ON.")
print()
print("Waiting 10 seconds...")
sleep(10)


# --------------------------------
# STEP 3
# LATCH
# --------------------------------

print()
print("STEP 3: LATCH")
print()
print("Transferring shift register to outputs...")
latch()

print()
print("LEDs should now ALL be OFF.")
print("Waiting 10 seconds...")
sleep(10)


# --------------------------------
# STEP 4
# Shift ones again WITHOUT latch
# --------------------------------

print()
print("STEP 4: SHIFT ONES WITHOUT LATCH")
print()

for i in range(8):
    print(f"Clock {i + 1}: DATA=1")
    shift_bit(1)

print()
print("LEDs should STILL be OFF.")
print()
print("Waiting 10 seconds...")
sleep(10)


# --------------------------------
# STEP 5
# LATCH ONES
# --------------------------------

print()
print("STEP 5: LATCH")
print()
print("LEDs should now ALL be ON.")
latch()

print()
print("Test complete.")

'''
All of the leds stayed on before, during, and after the test.

=========================
======================================
   SN74HC595 DIAGNOSTIC MONITOR
======================================

D2 = DATA
D3 = CLOCK
D4 = LATCH
D5 = Q7'

Waiting for Pi...

LATCH -> 0
CLOCK 1: DATA=1  Q7'=1
LATCH -> 1
LATCH -> 0
CLOCK 2: DATA=1  Q7'=1
CLOCK 3: DATA=1  Q7'=1
CLOCK 4: DATA=1  Q7'=1
LATCH -> 1
LATCH -> 0
CLOCK 5: DATA=1  Q7'=1
CLOCK 6: DATA=1  Q7'=1
LATCH -> 1
LATCH -> 0
'''