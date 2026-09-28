'''At this point the tests have shown that slowly changing state on the clock, latch, and data
will produce a result.  I asked ChatGPT for a program that is a simple counter with delays to
see if the speed is an issue. This is the resulting test'''


from fusion_hat.pin import Pin, Mode
import time

# 74HC595
SDI = Pin(17, mode=Mode.OUT)
RCLK = Pin(4, mode=Mode.OUT)
SRCLK = Pin(27, mode=Mode.OUT)

# Display digit select
DIG1 = Pin(23, mode=Mode.OUT)
DIG2 = Pin(24, mode=Mode.OUT)
DIG3 = Pin(25, mode=Mode.OUT)
DIG4 = Pin(12, mode=Mode.OUT)

# Common-anode segment codes
number = (
    0xC0,  # 0
    0xF9,  # 1
    0xA4,  # 2
    0xB0,  # 3
    0x99,  # 4
    0x92,  # 5
    0x82,  # 6
    0xF8,  # 7
    0x80,  # 8
    0x90,  # 9
)

def hc595_shift(data):
    print(f"    Sending 0x{data:02X}")

    for i in range(8):
        bit = 1 if (data & (0x80 >> i)) else 0
        SDI.value(bit)

        print(f"      bit {i}: {bit}")

        SRCLK.high()
        SRCLK.low()

    RCLK.high()
    RCLK.low()

def all_digits_off():
    DIG1.low()
    DIG2.low()
    DIG3.low()
    DIG4.low()

try:

    # Start with everything off
    all_digits_off()
    hc595_shift(0xFF)

    while True:

        for digit in range(10):

            print()
            print("=" * 40)
            print(f"DISPLAYING DIGIT: {digit}")
            print(f"SEGMENT CODE:    0x{number[digit]:02X}")
            print("=" * 40)

            # Turn everything off
            all_digits_off()

            # Load the segment pattern
            hc595_shift(number[digit])

            # Turn on FIRST digit only
            DIG1.high()

            print(f"First display position should show: {digit}")
            print("Waiting 2 seconds...")

            time.sleep(2)

            # Turn digit off
            DIG1.low()

            time.sleep(0.5)

except KeyboardInterrupt:
    print("\nStopping...")

finally:
    all_digits_off()
    hc595_shift(0xFF)

    SDI.close()
    RCLK.close()
    SRCLK.close()

    DIG1.close()
    DIG2.close()
    DIG3.close()
    DIG4.close()