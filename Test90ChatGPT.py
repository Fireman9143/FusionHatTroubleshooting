'''Another look at latching and Q7' memory with arduino from test 89'''

from fusion_hat.pin import Pin, Mode
from time import sleep

SDI  = Pin(17, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
MR   = Pin(22, mode=Mode.OUT)

SDI.low()
SRCLK.low()
RCLK.low()

print()
print("================================")
print("595 Q7' DIRECT VOLTAGE TEST")
print("================================")
print()

# ------------------------------------------------
# MR LOW = clear shift register
# ------------------------------------------------

print("STEP 1: CLEAR SHIFT REGISTER")
print("MR LOW")
print()

MR.low()
sleep(2)

print("MR HIGH")
MR.high()
sleep(2)

print("Shift register should now contain all zeroes.")
print()
print("Measure 595 PIN 9.")
print("Expected Q7' = approximately 0 V")
print()

input("Press ENTER after checking pin 9...")

# ------------------------------------------------
# Shift eight ZEROES
# ------------------------------------------------

print()
print("STEP 2: SHIFT 8 ZEROES")
print()

SDI.low()

for i in range(8):

    SRCLK.high()
    sleep(1)

    SRCLK.low()
    sleep(1)

    print(f"Clock {i + 1}")
    
    input("Check pin 9, then press ENTER...")

print()
print("DONE")