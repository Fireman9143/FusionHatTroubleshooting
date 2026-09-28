'''Another test for arduino test(87)'''


from fusion_hat.pin import Pin, Mode
from time import sleep

SDI = Pin(17, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)

# Start with everything LOW
SDI.low()
SRCLK.low()
RCLK.low()

print()
print("================================")
print("SIMPLE 595 TEST")
print("================================")
print()

# =========================================================
# TEST 1 - ALL ONES
# =========================================================

print("TEST 1")
print("DATA = HIGH")
print("CLOCK = 8 pulses")
print("LATCH = 1 pulse")
print()

SDI.high()

for i in range(8):
    print(f"CLOCK {i+1}")
    
    SRCLK.high()
    sleep(1)
    
    SRCLK.low()
    sleep(1)

print("8 clocks complete")
print("LATCH")

RCLK.high()
sleep(1)
RCLK.low()

print()
print("ALL LEDs should be ON.")
print("WAITING 10 SECONDS")
sleep(10)


# =========================================================
# TEST 2 - ALL ZEROES
# =========================================================

print()
print("TEST 2")
print("DATA = LOW")
print("CLOCK = 8 pulses")
print("LATCH = 1 pulse")
print()

SDI.low()

for i in range(8):
    print(f"CLOCK {i+1}")
    
    SRCLK.high()
    sleep(1)
    
    SRCLK.low()
    sleep(1)

print("8 clocks complete")
print("LATCH")

RCLK.high()
sleep(1)
RCLK.low()

print()
print("ALL LEDs should be OFF.")
print("WAITING 10 SECONDS")
sleep(10)

print()
print("TEST COMPLETE")

'''
All of the leds stayed on.

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
CLOCK 2: DATA=1  Q7'=1
CLOCK 3: DATA=1  Q7'=1
CLOCK 4: DATA=1  Q7'=1
CLOCK 5: DATA=1  Q7'=1
LATCH -> 1
CLOCK 6: DATA=1  Q7'=1
LATCH -> 0
CLOCK 7: DATA=1  Q7'=1
CLOCK 8: DATA=1  Q7'=1
  ---- 8 CLOCKS COMPLETE ----

CLOCK 9: DATA=1  Q7'=1
CLOCK 10: DATA=1  Q7'=1
CLOCK 11: DATA=1  Q7'=1
CLOCK 12: DATA=0  Q7'=1
LATCH -> 1
CLOCK 13: DATA=0  Q7'=1
LATCH -> 0
'''