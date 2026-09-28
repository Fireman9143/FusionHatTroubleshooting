'''Another look at shifting Q7' pin 9'''


from fusion_hat.pin import Pin, Mode
from time import sleep

SRCLK = Pin(27, mode=Mode.OUT)

SRCLK.low()

for i in range(9):
    print(f"Clock {i + 1}")

    SRCLK.high()
    sleep(1)

    SRCLK.low()
    sleep(1)

print("Done")