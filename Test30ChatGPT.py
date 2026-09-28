'''This test checked that the fusion hat could control all clocking and latching, measuring 
pin 15 to verify state'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)

# Start LOW
SDI.low()
SRCLK.low()
RCLK.low()

# Shift eight 1s
print("Shifting 8 HIGH bits...")

for i in range(8):
    SDI.high()

    SRCLK.high()
    time.sleep(0.2)

    SRCLK.low()
    time.sleep(0.2)

print("8 bits shifted.")
print("Q0 should currently still be LOW.")
time.sleep(2)

# Latch
print("Latching...")
RCLK.high()
time.sleep(1)
RCLK.low()

print("Q0 should now be HIGH.")
time.sleep(5)