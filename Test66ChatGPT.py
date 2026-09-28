'''This is another attempt to use .value() instead of .low()/.high()'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)

def clock():
    SRCLK.value(1)
    time.sleep(1)
    SRCLK.value(0)
    time.sleep(1)

# Start known state
SDI.value(1)
SRCLK.value(0)
RCLK.value(0)

print("Sending 0xFF...")
for i in range(8):
    print(f"  bit {i}: DATA HIGH")
    SDI.value(1)
    time.sleep(1)
    clock()

print("Latching 0xFF...")
RCLK.value(1)
time.sleep(1)
RCLK.value(0)
time.sleep(3)

print("Now pin 15 should be HIGH.")
input("Measure pin 15, then press ENTER...")

print()
print("Sending 0xFE...")
print("This puts Q0 LOW and Q1-Q7 HIGH.")

# 0xFE = 11111110
bits = [1, 1, 1, 1, 1, 1, 1, 0]

for i, bit in enumerate(bits):
    print(f"  bit {i}: DATA {'HIGH' if bit else 'LOW'}")

    SDI.value(bit)
    time.sleep(1)

    print("    CLOCK HIGH")
    SRCLK.value(1)
    time.sleep(1)

    print("    CLOCK LOW")
    SRCLK.value(0)
    time.sleep(1)

print("Latching 0xFE...")
RCLK.value(1)
time.sleep(1)
RCLK.value(0)

print()
print("0xFE is now latched.")
print("Measure pin 15.")
input("Press ENTER when finished...")

SDI.value(0)
SRCLK.value(0)
RCLK.value(0)

SDI.close()
SRCLK.close()
RCLK.close()