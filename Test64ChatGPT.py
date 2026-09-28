'''The last test produced a blank display, so this test is even slower'''


from fusion_hat.pin import Pin, Mode
import time

SDI = Pin(17, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

def shift_slow(data):

    print(f"\nSending 0x{data:02X}")

    for i in range(8):
        bit = 1 if (data & (0x80 >> i)) else 0

        print(f"Bit {i}: {bit}")
        SDI.value(bit)

        print("  Data set. Waiting...")
        time.sleep(1)

        print("  Clock HIGH")
        SRCLK.high()
        time.sleep(1)

        print("  Clock LOW")
        SRCLK.low()
        time.sleep(1)

    print("All 8 bits shifted.")
    print("Waiting before latch...")
    time.sleep(2)

    print("LATCH HIGH")
    RCLK.high()
    time.sleep(1)

    print("LATCH LOW")
    RCLK.low()

    print("Latch complete.")
    time.sleep(3)


try:
    print("Starting 0x00 test")
    shift_slow(0x00)

    print("\nStarting 0xFF test")
    shift_slow(0xFF)

finally:
    SDI.low()
    SRCLK.low()
    RCLK.low()

    SDI.close()
    RCLK.close()
    SRCLK.close()