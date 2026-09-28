'''This is now going back to registering bits in the chip and watching pin 15'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

def shift(data):
    for _ in range(8):
        SDI.value(1 if data & 0x80 else 0)

        SRCLK.low()
        SRCLK.high()

        data <<= 1

    SRCLK.low()

def latch():
    RCLK.low()
    time.sleep(0.1)
    RCLK.high()
    time.sleep(0.1)
    RCLK.low()

# --------------------------------
# Put eight 1s into shift register
# --------------------------------

print("Sending 0xFF")

shift(0xFF)

print("Latching 0xFF")
latch()

time.sleep(3)

print("Q0 should be HIGH.")
print("Pin 15 should be about 3.3 V.")

time.sleep(3)

# --------------------------------
# Put eight 0s into shift register
# --------------------------------

print("Sending 0x00")

shift(0x00)

print("Latching 0x00")
latch()

time.sleep(3)

print("Q0 should now be LOW.")
print("Pin 15 should be about 0 V.")

time.sleep(10)