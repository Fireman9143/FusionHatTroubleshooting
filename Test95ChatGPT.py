'''Another test for arduino monitor test 94'''



from fusion_hat import Pin, Mode
import time


# ============================================================
# 74HC595 CONNECTIONS
#
# Raspberry Pi GPIO17 -> 595 pin 14 DATA
# Raspberry Pi GPIO27 -> 595 pin 11 CLOCK
# Raspberry Pi GPIO4  -> 595 pin 12 LATCH
#
# 595 pin 10 -> 3.3V  (SRCLR)
# 595 pin 13 -> GND   (OE)
# 595 pin 16 -> 3.3V  (VCC)
# 595 pin 8  -> GND
# ============================================================


DATA = Pin(17, mode=Mode.OUT)
CLOCK = Pin(27, mode=Mode.OUT)
LATCH = Pin(4, mode=Mode.OUT)


# ============================================================
# INITIAL STATE
# ============================================================

DATA.low()
CLOCK.low()
LATCH.low()

time.sleep(2)


# ============================================================
# CLOCK ONE BIT
# ============================================================

def clock_bit(bit):

    if bit == 1:
        DATA.high()
    else:
        DATA.low()

    print("DATA =", bit)

    time.sleep(0.5)

    print("  CLOCK HIGH")
    CLOCK.high()

    time.sleep(0.5)

    print("  CLOCK LOW")
    CLOCK.low()

    time.sleep(0.5)


# ============================================================
# LATCH
# ============================================================

def latch():

    print()
    print("LATCH HIGH")
    LATCH.high()

    time.sleep(1)

    print("LATCH LOW")
    LATCH.low()

    time.sleep(1)


# ============================================================
# SEND A DESIRED Q7-Q0 PATTERN
#
# The pattern is written in the normal way:
#
#     Q7 Q6 Q5 Q4 Q3 Q2 Q1 Q0
#
# The function reverses it because the 595 shifts:
#
#     DATA -> Q0 -> Q1 -> ... -> Q7
# ============================================================

def send_pattern(pattern):

    print()
    print("========================================")
    print("DESIRED OUTPUT:")
    print("Q7 Q6 Q5 Q4 Q3 Q2 Q1 Q0")
    print("   " + "  ".join(pattern))
    print("========================================")
    print()

    # Reverse the desired Q7-Q0 pattern.
    # This gives the order the 595 must receive.
    bits_to_send = pattern[::-1]

    print("Bits sent to DATA:")
    print(" ".join(bits_to_send))
    print()

    for bit in bits_to_send:
        clock_bit(int(bit))

    print()
    print("All 8 clock pulses complete.")
    print("Q outputs should still not change until LATCH.")
    print()

    time.sleep(2)

    latch()

    print()
    print("OUTPUT PATTERN SHOULD NOW BE:")
    print("Q7 Q6 Q5 Q4 Q3 Q2 Q1 Q0")
    print("   " + "  ".join(pattern))
    print()

    time.sleep(4)


# ============================================================
# TEST 1
# ALL OUTPUTS LOW
# ============================================================

print()
print("########################################")
print("# TEST 1")
print("# ALL OUTPUTS LOW")
print("########################################")

send_pattern("00000000")


# ============================================================
# TEST 2
# ONLY Q7 HIGH
# ============================================================

print()
print("########################################")
print("# TEST 2")
print("# ONLY Q7 HIGH")
print("########################################")

send_pattern("10000000")


# ============================================================
# TEST 3
# ALTERNATING
# ============================================================

print()
print("########################################")
print("# TEST 3")
print("# ALTERNATING OUTPUTS")
print("########################################")

send_pattern("10101010")


# ============================================================
# FINISHED
# ============================================================

print()
print("########################################")
print("# TESTS COMPLETE")
print("########################################")

DATA.low()
CLOCK.low()
LATCH.low()

'''
================================
74HC595 CHANGE-ONLY MONITOR
================================
Waiting for changes...

CLOCK  : 0 -> 1
Q7'    : 0 -> 1
CLOCK  : 1 -> 0
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
LATCH  : 0 -> 1
Q1     : 1 -> 0
Q2     : 0 -> 1
Q3     : 1 -> 0
Q4     : 0 -> 1
Q6     : 1 -> 0
Q7     : 0 -> 1
LATCH  : 1 -> 0
CLOCK  : 0 -> 1
Q7'    : 1 -> 0
CLOCK  : 1 -> 0
CLOCK  : 0 -> 1
DATA   : 0 -> 1
CLOCK  : 1 -> 0
LATCH  : 0 -> 1
Q2     : 1 -> 0
Q3     : 0 -> 1
Q4     : 1 -> 0
Q5     : 0 -> 1
Q7     : 1 -> 0
LATCH  : 1 -> 0
DATA   : 1 -> 0
CLOCK  : 0 -> 1
DATA   : 0 -> 1
DATA   : 1 -> 0
CLOCK  : 1 -> 0
CLOCK  : 0 -> 1
DATA   : 0 -> 1
DATA   : 1 -> 0
CLOCK  : 1 -> 0
CLOCK  : 0 -> 1
DATA   : 0 -> 1
DATA   : 1 -> 0
CLOCK  : 1 -> 0
CLOCK  : 0 -> 1
DATA   : 0 -> 1
CLOCK  : 1 -> 0
LATCH  : 0 -> 1
Q3     : 1 -> 0
Q4     : 0 -> 1
Q5     : 1 -> 0
Q6     : 0 -> 1
LATCH  : 1 -> 0
DATA   : 1 -> 0

I asked Claude AI about this same problem. 
It suggested that the problem may be in memory handling.  
I have added a 0.1uF capacitor across the 3.3v and ground rails, 
added a time.sleep(0.0000001) between the SRCLK.high() and SRCLK.low() in both the 
clearDisplay() and hc595_shift() functions.  Claude also gave me a new list of codes 
for the number tuple, and had me wire 595 pin 10 to GPIO 26 so I can clear memory when 
the program first runs.  Now, every time I run the program I get every segment of every 
digit except A to light up.

'''