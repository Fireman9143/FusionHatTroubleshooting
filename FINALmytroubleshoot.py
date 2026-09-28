from fusion_hat.pin import Pin, Mode
import time

print("Creating pin objects...")
SDI = Pin(6, mode=Mode.OUT)      # Serial Data Input
RCLK = Pin(13, mode=Mode.OUT)      # Register Clock
SRCLK = Pin(5, mode=Mode.OUT)    # Shift Register Clock
MEMCLEAR = Pin(22, mode=Mode.OUT) # Low to clear 595 shift register (MR/SRCLR)

placePin = [Pin(pin, mode=Mode.OUT) for pin in (23, 24, 25, 12)]
print("Pin objects created successfully.")

# Segment codes for 0-9, matching your confirmed SunFounder pinout
# (Q0=b, Q1=c, Q2=d, Q3=e, Q4=f, Q5=g, Q6=DP, Q7=a)
#number = (0x60, 0xfc, 0x52, 0x58, 0xcc, 0x49, 0x41, 0x7c, 0x40, 0x48)
#number = (0xc0, 0xf9, 0xa4, 0xb0, 0x99, 0x92, 0x82, 0xf8, 0x80, 0x90)
number = (0x03, 0x00, 0xff, 0x00)
def clearDisplay():
    for _ in range(8):
        SDI.high()
        time.sleep(0.05)
        SRCLK.high()
        time.sleep(0.05)
        SRCLK.low()
        time.sleep(0.05)
    RCLK.high()
    time.sleep(0.05)
    RCLK.low()

placePin[0].high()
placePin[1].low()
placePin[2].low()
placePin[3].low()

try:
    print("Pulsing MEMCLEAR (595 master reset)...")
    MEMCLEAR.low()
    time.sleep(0.001)
    MEMCLEAR.high()
    print("MEMCLEAR pulse complete.")
    for _ in range(8):
        SDI.low()
        time.sleep(0.05)
        SRCLK.high()
        time.sleep(0.05)
        SRCLK.low()
        time.sleep(0.05)
    RCLK.high()
    time.sleep(0.05)
    RCLK.low()
    print("All segments should be on")
    time.sleep(5)
    for _ in range(8):
        SDI.high()
        time.sleep(0.05)
        SRCLK.high()
        time.sleep(0.05)
        SRCLK.low()
        time.sleep(0.05)
    RCLK.high()
    time.sleep(0.05)
    RCLK.low()
    print("all segments should be off")
    time.sleep(5)
    for _ in range(8):
        SDI.low()
        time.sleep(0.05)
        SRCLK.high()
        time.sleep(0.05)
        SRCLK.low()
        time.sleep(0.05)
    RCLK.high()
    time.sleep(0.05)
    RCLK.low()
    print("All segments should be on")
    time.sleep(5)
    for _ in range(8):
        SDI.high()
        time.sleep(0.05)
        SRCLK.high()
        time.sleep(0.05)
        SRCLK.low()
        time.sleep(0.05)
    RCLK.high()
    time.sleep(0.05)
    RCLK.low()
    print("all segments should be off")
    time.sleep(5)

except KeyboardInterrupt:
    print("\nStopped by user (Ctrl+C).")

except Exception as e:
    print(f"\n*** ERROR: {type(e).__name__}: {e} ***")

finally:
    print("Cleaning up GPIO...")
    for device in [SDI, RCLK, SRCLK, MEMCLEAR] + placePin:
        try:
            device.close()
        except Exception:
            pass
    print("Done.")