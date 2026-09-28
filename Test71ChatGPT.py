'''This test was shifting one bit through the register and watching Q0'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)

SDI.low()
SRCLK.low()
RCLK.low()

def clock():
    SRCLK.high()
    time.sleep(1)
    SRCLK.low()
    time.sleep(1)

print()
print("595 Q0 TEST")
print("===========")
print()
print("First we will shift 00000000.")
print("Then we will latch it.")
print("Measure Q0 = 595 pin 15.")
print()

# Shift eight zeros
for i in range(8):
    print(f"Clock {i+1}: DATA = 0")
    SDI.low()
    time.sleep(1)
    clock()

print("Eight zeros shifted.")
print()
print("Now LATCH.")
RCLK.high()
time.sleep(2)
RCLK.low()
time.sleep(2)

print()
print("Measure pin 15 (Q0).")
input("Press ENTER when ready for the next test...")

print()
print("Now we will shift 11111111.")
print()

# Shift eight ones
for i in range(8):
    print(f"Clock {i+1}: DATA = 1")
    SDI.high()
    time.sleep(1)
    clock()

print("Eight ones shifted.")
print()
print("Now LATCH.")
RCLK.high()
time.sleep(2)
RCLK.low()
time.sleep(2)

print()
print("Measure pin 15 (Q0).")
input("Press ENTER to finish.")

SDI.low()
SRCLK.low()
RCLK.low()

SDI.close()
SRCLK.close()
RCLK.close()