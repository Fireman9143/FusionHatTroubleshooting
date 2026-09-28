'''Manual clocking with measurements of Q7' to watch changes'''


from fusion_hat.pin import Pin, Mode
from time import sleep

SRCLK = Pin(27, mode=Mode.OUT)

SRCLK.low()

print("DATA pin 14 is physically HIGH.")
print("MR pin 10 is HIGH.")
print()
print("Starting clock test.")

for i in range(8):

    print(f"Clock {i + 1}")

    SRCLK.high()
    sleep(2)

    SRCLK.low()
    sleep(2)

print()
print("8 clocks complete.")