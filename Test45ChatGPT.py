'''This test is going back to check pins 11, 12, and 14 are clocking and registering correctly. 
After this test, more manual latching was done to confirm chip operation compared to pin control'''


from fusion_hat.pin import Pin, Mode
import time

DS = Pin(17, mode=Mode.OUT)
SHCP = Pin(27, mode=Mode.OUT)
STCP = Pin(4, mode=Mode.OUT)

DS.low()
SHCP.low()
STCP.low()

print("DS LOW, SHCP LOW, STCP LOW")
print("Measure pins 14, 11, 12.")
time.sleep(5)

DS.high()
print("DS HIGH")
print("Pin 14 should now be ~3.3V.")
time.sleep(5)

SHCP.high()
print("SHCP HIGH")
print("Pin 11 should now be ~3.3V.")
time.sleep(5)

STCP.high()
print("STCP HIGH")
print("Pin 12 should now be ~3.3V.")
time.sleep(5)

STCP.low()
SHCP.low()
DS.low()

DS.close()
SHCP.close()
STCP.close()