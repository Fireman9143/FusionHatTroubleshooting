'''This test is to latch all 0's and measure pin 15 to see if it registers correctly'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

# Start everything LOW
SDI.low()
RCLK.low()
SRCLK.low()

print("Shifting eight ZERO bits...")

for i in range(8):
    SDI.low()

    # Rising edge clocks the zero into the shift register
    SRCLK.high()
    time.sleep(0.1)
    SRCLK.low()
    time.sleep(0.1)

print("Eight zeros shifted.")
print("Now latching...")

# Transfer shift register into output register
RCLK.high()
time.sleep(0.2)
RCLK.low()

print("Latch complete.")
print("Measure pin 15 now.")

# Leave everything in a known state
SDI.low()
SRCLK.low()
RCLK.low()

time.sleep(10)

SDI.close()
SRCLK.close()
RCLK.close()