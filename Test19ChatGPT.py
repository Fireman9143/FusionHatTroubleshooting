'''This test starts to check if clocking is making it through, while measuring pin 15 state'''

from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

SDI.low()
SRCLK.low()
RCLK.low()

def clock():
    SRCLK.high()
    time.sleep(0.2)
    SRCLK.low()
    time.sleep(0.2)

def latch():
    RCLK.high()
    time.sleep(0.2)
    RCLK.low()

# Clear everything
for _ in range(8):
    clock()

latch()

print("Cleared. Q0 should be LOW.")
time.sleep(2)

# Put a single 1 into the shift register
SDI.high()

for i in range(8):
    print("Clock", i + 1)
    clock()

    # Latch after every clock so we can watch the output move
    latch()

    time.sleep(1)

SDI.low()

print("Finished.")
time.sleep(5)