'''This is another test to confirm clocking and latching, monitoring pin 15'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)

# Start everything LOW
SDI.low()
SRCLK.low()
RCLK.low()

print("Clearing shift register with 8 zeros...")

for _ in range(8):
    SRCLK.high()
    time.sleep(0.1)
    SRCLK.low()
    time.sleep(0.1)

# Make sure latch is low
RCLK.low()

print("Latch cleared.")
time.sleep(2)

print("Putting ONE HIGH bit on DS...")
SDI.high()
time.sleep(2)

print("Clocking ONE bit...")
SRCLK.high()
time.sleep(1)
SRCLK.low()
time.sleep(2)

print("Now latching...")
RCLK.high()
time.sleep(1)
RCLK.low()

print("Done. Q0 should be HIGH.")
time.sleep(5)