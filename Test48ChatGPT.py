'''After testing clock speeds, this is another test to see if Q0-Q7 respond correctly'''


from fusion_hat.pin import Pin, Mode
import time

DS = Pin(17, mode=Mode.OUT)
SHCP = Pin(27, mode=Mode.OUT)
STCP = Pin(4, mode=Mode.OUT)

DS.low()
SHCP.low()
STCP.low()

# Shift 11111111
for i in range(8):
    DS.high()
    time.sleep(0.001)

    SHCP.high()
    time.sleep(0.001)

    SHCP.low()
    time.sleep(0.001)

# Latch
STCP.high()
time.sleep(0.001)
STCP.low()

print("Eight ones shifted and latched.")
print("Q0-Q7 should ALL be HIGH.")

time.sleep(5)

DS.close()
SHCP.close()
STCP.close()