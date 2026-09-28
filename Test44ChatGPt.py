'''This test now checked Q0-Q7 and pins 10 and 13'''


from fusion_hat.pin import Pin, Mode
import time

DS = Pin(17, mode=Mode.OUT)
SHCP = Pin(27, mode=Mode.OUT)
STCP = Pin(4, mode=Mode.OUT)

DS.low()
SHCP.low()
STCP.low()

# Make absolutely sure the data is 00000000
for _ in range(8):
    DS.low()
    SHCP.high()
    SHCP.low()

# Latch 00000000
STCP.high()
STCP.low()

print("Latched 00000000")
print("Measure Q0-Q7. All should be LOW.")
print("Also measure MR (pin 10) and OE (pin 13).")
time.sleep(10)

DS.close()
SHCP.close()
STCP.close()