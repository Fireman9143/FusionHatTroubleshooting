'''I asked chatGPT to start over with a fresh approach to troubleshooting, assuming the things
we have proven so far. After manually operating the 595, this test was next with arduino monitor'''



from fusion_hat import Pin, Mode
import time


# ============================================================
# Raspberry Pi -> 74HC595
#
# GPIO17 -> 595 pin 14  DATA / DS
# GPIO27 -> 595 pin 11  CLOCK / SHCP
# GPIO4  -> 595 pin 12  LATCH / STCP
#
# 595 pin 10 -> 3.3V  (SRCLR / MR)
# 595 pin 13 -> GND   (OE)
# 595 pin 16 -> 3.3V  (VCC)
# 595 pin 8  -> GND
# ============================================================


DATA = Pin(17, mode=Mode.OUT)
CLOCK = Pin(27, mode=Mode.OUT)
LATCH = Pin(4, mode=Mode.OUT)


# ============================================================
# Make sure everything starts LOW
# ============================================================

DATA.low()
CLOCK.low()
LATCH.low()

time.sleep(2)


# ============================================================
# Helper functions
# ============================================================

def clock_pulse():
    """
    One complete rising/falling clock pulse.
    """
    CLOCK.high()
    time.sleep(0.25)

    CLOCK.low()
    time.sleep(0.25)


def latch_pulse():
    """
    Transfer the shift register into the output register.
    """
    LATCH.high()
    time.sleep(0.25)

    LATCH.low()
    time.sleep(0.25)


def send_bit(bit):
    """
    Put one bit on DATA and clock it into the 595.
    """

    if bit:
        DATA.high()
    else:
        DATA.low()

    print(f"DATA = {bit}")

    time.sleep(0.5)

    print("CLOCK HIGH")
    CLOCK.high()
    time.sleep(0.5)

    print("CLOCK LOW")
    CLOCK.low()
    time.sleep(0.5)


def send_byte(bits):
    """
    Send eight bits, MSB first.
    """

    print()
    print("----------------------------------------")
    print("Sending:", bits)
    print("----------------------------------------")

    for bit in bits:
        send_bit(int(bit))

    print()
    print("All 8 bits shifted.")
    print("The Q outputs should NOT change yet.")
    print()

    time.sleep(2)

    print("LATCH HIGH")
    LATCH.high()
    time.sleep(1)

    print("LATCH LOW")
    LATCH.low()
    time.sleep(1)

    print("LATCH complete.")
    print()

    time.sleep(3)


# ============================================================
# TEST 1
# Clear the outputs
# ============================================================

print()
print("========================================")
print("TEST 1 - CLEAR OUTPUTS")
print("========================================")
print()
print("Sending 00000000")
print()

send_byte("00000000")


# ============================================================
# TEST 2
# Send 10000000
# ============================================================

print()
print("========================================")
print("TEST 2 - ONE HIGH BIT")
print("========================================")
print()
print("Sending 10000000")
print()

send_byte("10000000")


# ============================================================
# TEST 3
# Send 01000000
# ============================================================

print()
print("========================================")
print("TEST 3")
print("========================================")
print()
print("Sending 01000000")
print()

send_byte("01000000")


# ============================================================
# TEST 4
# Send 00100000
# ============================================================

print()
print("========================================")
print("TEST 4")
print("========================================")
print()
print("Sending 00100000")
print()

send_byte("00100000")


# ============================================================
# TEST 5
# Send 10101010
# ============================================================

print()
print("========================================")
print("TEST 5 - ALTERNATING BITS")
print("========================================")
print()
print("Sending 10101010")
print()

send_byte("10101010")


# ============================================================
# TEST 6
# Send 01010101
# ============================================================

print()
print("========================================")
print("TEST 6 - ALTERNATING BITS")
print("========================================")
print()
print("Sending 01010101")
print()

send_byte("01010101")


# ============================================================
# TEST 7
# All outputs HIGH
# ============================================================

print()
print("========================================")
print("TEST 7 - ALL HIGH")
print("========================================")
print()
print("Sending 11111111")
print()

send_byte("11111111")


# ============================================================
# TEST 8
# All outputs LOW
# ============================================================

print()
print("========================================")
print("TEST 8 - ALL LOW")
print("========================================")
print()
print("Sending 00000000")
print()

send_byte("00000000")


# ============================================================
# Finished
# ============================================================

print()
print("========================================")
print("ALL TESTS COMPLETE")
print("========================================")

DATA.low()
CLOCK.low()
LATCH.low()


'''

================================
74HC595 CHANGE-ONLY MONITOR
================================
Waiting for changes...

CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
LATCH  : 0 -> 1
Q2     : 1 -> 0
Q5     : 0 -> 1
Q6     : 0 -> 1
LATCH  : 1 -> 0
DATA   : 0 -> 1
CLOCK  : 0 -> 1
Q7'    : 0 -> 1
DATA   : 1 -> 0
CLOCK  : 1 -> 0
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
LATCH  : 0 -> 1
Q0     : 0 -> 1
Q1     : 1 -> 0
Q2     : 0 -> 1
Q3     : 1 -> 0
Q7     : 0 -> 1
LATCH  : 1 -> 0
CLOCK  : 0 -> 1
DATA   : 0 -> 1
DATA   : 1 -> 0
CLOCK  : 1 -> 0
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
LATCH  : 0 -> 1
Q0     : 1 -> 0
Q1     : 0 -> 1
Q2     : 1 -> 0
Q3     : 0 -> 1
Q4     : 1 -> 0
LATCH  : 1 -> 0
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
CLOCK  : 0 -> 1
DATA   : 0 -> 1
DATA   : 1 -> 0
CLOCK  : 1 -> 0
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
LATCH  : 0 -> 1
Q1     : 1 -> 0
Q2     : 0 -> 1
Q3     : 1 -> 0
Q4     : 0 -> 1
Q5     : 1 -> 0
LATCH  : 1 -> 0
DATA   : 0 -> 1
CLOCK  : 0 -> 1
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
DATA   : 1 -> 0
CLOCK  : 1 -> 0
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
LATCH  : 0 -> 1
Q0     : 0 -> 1
Q2     : 1 -> 0
Q3     : 0 -> 1
Q4     : 1 -> 0
Q5     : 0 -> 1
Q6     : 1 -> 0
LATCH  : 1 -> 0
CLOCK  : 0 -> 1
Q7'    : 1 -> 0
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
Q0     : 1 -> 0
Q1     : 0 -> 1
Q3     : 1 -> 0
Q4     : 0 -> 1
Q5     : 1 -> 0
Q6     : 0 -> 1
Q7     : 1 -> 0
LATCH  : 1 -> 0
CLOCK  : 0 -> 1
Q7'    : 0 -> 1
CLOCK  : 1 -> 0
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
LATCH  : 0 -> 1
Q0     : 0 -> 1
Q1     : 1 -> 0
Q2     : 0 -> 1
Q4     : 1 -> 0
Q5     : 0 -> 1
Q6     : 1 -> 0
Q7     : 0 -> 1
LATCH  : 1 -> 0
DATA   : 1 -> 0
CLOCK  : 0 -> 1
Q7'    : 1 -> 0
CLOCK  : 1 -> 0
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
LATCH  : 0 -> 1
Q0     : 1 -> 0
Q1     : 0 -> 1
Q2     : 1 -> 0
Q3     : 0 -> 1
Q5     : 1 -> 0
Q6     : 0 -> 1
Q7     : 1 -> 0
LATCH  : 1 -> 0
'''