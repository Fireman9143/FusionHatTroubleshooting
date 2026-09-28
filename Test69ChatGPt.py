'''I asked ChatGPT for a way to monitor pin 11 for clock changes while also checking on Q7'
and this is the result'''


from fusion_hat.pin import Pin, Mode
import time

SRCLK = Pin(27, mode=Mode.OUT)

SRCLK.low()

print("GPIO27 -> 595 pin 11 clock test")
print("Probe 595 pin 11 with your multimeter.")
print()

for i in range(10):
    print(f"Clock {i+1}: HIGH")
    SRCLK.high()
    time.sleep(2)

    print(f"Clock {i+1}: LOW")
    SRCLK.low()
    time.sleep(2)

print("Done.")

SRCLK.low()
SRCLK.close()