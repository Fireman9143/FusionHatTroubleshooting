'''This test was to check the status of Q0-Q7 after shifting'''


from fusion_hat.pin import Pin, Mode
import time

DS = Pin(17, mode=Mode.OUT)
SHCP = Pin(27, mode=Mode.OUT)
STCP = Pin(4, mode=Mode.OUT)

DS.low()
SHCP.low()
STCP.low()

# Shift 00000001
for bit in [0, 0, 0, 0, 0, 0, 0, 1]:
    DS.value(bit)
    SHCP.high()
    SHCP.low()

# Transfer shift register -> output register
STCP.high()
STCP.low()

print("0x01 latched. Q0 (pin 15) should be HIGH.")
print("Q1-Q7 should be LOW.")

time.sleep(10)

DS.close()
SHCP.close()
STCP.close()