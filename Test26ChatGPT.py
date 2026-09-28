'''This test is methodically shifting bits, latching them, and measuring pin 15 state'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)

# Make sure clock and latch start LOW
SDI.low()
SRCLK.low()
RCLK.low()

def shift_byte(data):
    for i in range(8):
        bit = (data >> (7 - i)) & 1

        if bit:
            SDI.high()
        else:
            SDI.low()

        SRCLK.high()
        time.sleep(0.1)
        SRCLK.low()
        time.sleep(0.1)

def latch():
    RCLK.low()
    time.sleep(0.2)
    RCLK.high()
    time.sleep(0.2)
    RCLK.low()
    time.sleep(0.2)

print("Sending 00000000")
shift_byte(0x00)
latch()

print("Q0 should now be LOW")
time.sleep(3)

print("Sending 11111111")
shift_byte(0xFF)
latch()

print("Q0 should now be HIGH")
time.sleep(3)

print("Sending 00000000 again")
shift_byte(0x00)
latch()

print("Q0 should now be LOW")
time.sleep(3)