'''This test is checking how python is changing state within the module'''


from fusion_hat.pin import Pin, Mode
import time

DS = Pin(17, mode=Mode.OUT)
SHCP = Pin(27, mode=Mode.OUT)
STCP = Pin(4, mode=Mode.OUT)

DS.low()
SHCP.low()
STCP.low()

# Shift eight ZERO bits, slowly.
for i in range(8):
    DS.low()
    time.sleep(0.1)

    SHCP.high()
    time.sleep(0.1)

    SHCP.low()
    time.sleep(0.1)

# Latch
STCP.high()
time.sleep(0.1)
STCP.low()

print("Eight zeros shifted and latched.")
print("Q0-Q7 should ALL be LOW.")

time.sleep(10)

DS.close()
SHCP.close()
STCP.close()