'''This test was meant to introduce delays in the clock pulses, and the time was changed to
shorter (0.001) and shorter (0.0001) intervals to see if the pins could handle the speed'''


from fusion_hat.pin import Pin, Mode
import time

DS = Pin(17, mode=Mode.OUT)
SHCP = Pin(27, mode=Mode.OUT)
STCP = Pin(4, mode=Mode.OUT)

DS.low()
SHCP.low()
STCP.low()

for i in range(8):
    DS.low()
    time.sleep(0.01)

    SHCP.high()
    time.sleep(0.01)

    SHCP.low()
    time.sleep(0.01)

STCP.high()
time.sleep(0.01)
STCP.low()

print("Eight zeros shifted and latched.")
print("Q0-Q7 should all be LOW.")

time.sleep(5)

DS.close()
SHCP.close()
STCP.close()