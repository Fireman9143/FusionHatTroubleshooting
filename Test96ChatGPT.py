'''ChatGPT and Claude are starting to get snippets of the tests that each AI is running.  
This is the next python test from ChatGPT after analyzing Claude results'''



#!/usr/bin/env python3

from fusion_hat.pin import Pin, Mode
import time


# ============================================================
# 74HC595 PINS
# ============================================================

SDI = Pin(17, mode=Mode.OUT)       # 595 pin 14 - DATA
RCLK = Pin(4, mode=Mode.OUT)       # 595 pin 12 - LATCH
SRCLK = Pin(27, mode=Mode.OUT)     # 595 pin 11 - CLOCK

# IMPORTANT:
# Use the GPIO that is ACTUALLY wired to 595 pin 10.
#
# If your wire is GPIO26:
MEMCLEAR = Pin(26, mode=Mode.OUT)


# ============================================================
# DISPLAY DIGIT SELECT
#
# GPIO23 -> display pin 12
# GPIO24 -> display pin 9
# GPIO25 -> display pin 8
# GPIO12 -> display pin 6
# ============================================================

placePin = [
    Pin(23, mode=Mode.OUT),
    Pin(24, mode=Mode.OUT),
    Pin(25, mode=Mode.OUT),
    Pin(12, mode=Mode.OUT)
]


# ============================================================
# COMMON-ANODE SEGMENT CODES
#
# Q0 -> A
# Q1 -> B
# Q2 -> C
# Q3 -> D
# Q4 -> E
# Q5 -> F
# Q6 -> G
# Q7 -> DP
#
# LOW  = segment ON
# HIGH = segment OFF
# ============================================================

number = (
    0xC0,   # 0
    0xF9,   # 1
    0xA4,   # 2
    0xB0,   # 3
    0x99,   # 4
    0x92,   # 5
    0x82,   # 6
    0xF8,   # 7
    0x80,   # 8
    0x90    # 9
)


# ============================================================
# INITIALIZE
# ============================================================

SDI.low()
RCLK.low()
SRCLK.low()

for pin in placePin:
    pin.low()

# SRCLR is ACTIVE LOW.
# Normally it must be HIGH.
MEMCLEAR.high()

time.sleep(1)


# ============================================================
# CLEAR THE 74HC595
# ============================================================

def clear_display():

    print("Clearing 595...")

    # Pull SRCLR LOW.
    MEMCLEAR.low()

    time.sleep(0.01)

    # Return SRCLR HIGH.
    MEMCLEAR.high()

    time.sleep(0.01)

    # Make sure clocks are LOW.
    SRCLK.low()
    RCLK.low()

    print("595 cleared.")


# ============================================================
# SHIFT ONE BYTE INTO THE 595
# ============================================================

def hc595_shift(data):

    print(f"Sending 0x{data:02X}")

    for i in range(8):

        bit = 1 if (data & (0x80 >> i)) else 0

        if bit:
            SDI.high()
        else:
            SDI.low()

        print(f"  Bit {i}: {bit}")

        # Clock rising edge
        SRCLK.high()
        time.sleep(0.001)

        # Clock falling edge
        SRCLK.low()
        time.sleep(0.001)

    # Transfer shift register to output register.
    print("  LATCH")

    RCLK.high()
    time.sleep(0.001)

    RCLK.low()
    time.sleep(0.001)


# ============================================================
# SELECT ONE DIGIT
# ============================================================

def pick_digit(digit):

    # Turn all digits OFF.
    for pin in placePin:
        pin.low()

    # Turn selected digit ON.
    placePin[digit].high()


# ============================================================
# TEST
# ============================================================

try:

    print()
    print("========================================")
    print("74HC595 FIXED DISPLAY TEST")
    print("========================================")
    print()

    clear_display()

    # --------------------------------------------------------
    # TEST 1
    # Display zero on digit 1.
    # --------------------------------------------------------

    print("TEST 1: Displaying 0 on digit 1")

    pick_digit(0)

    hc595_shift(number[0])

    time.sleep(5)


    # --------------------------------------------------------
    # TEST 2
    # Display eight on digit 1.
    # --------------------------------------------------------

    print("TEST 2: Displaying 8 on digit 1")

    hc595_shift(number[8])

    time.sleep(5)


    # --------------------------------------------------------
    # TEST 3
    # Display one on digit 1.
    # --------------------------------------------------------

    print("TEST 3: Displaying 1 on digit 1")

    hc595_shift(number[1])

    time.sleep(5)


    print()
    print("TEST COMPLETE.")


except KeyboardInterrupt:

    print()
    print("Stopping...")


finally:

    # Turn display digits OFF.
    for pin in placePin:
        pin.low()

    SDI.low()
    SRCLK.low()
    RCLK.low()

    MEMCLEAR.high()

    print("GPIO returned to safe state.")

