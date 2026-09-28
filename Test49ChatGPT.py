'''This test is only testing pin 14 for the data signal.  During previous tests pin 14
had been attached to 3.3v to force high bits.  There is a little testing that was not
completed once this was found'''


from fusion_hat.pin import Pin, Mode
import time

DS = Pin(17, mode=Mode.OUT)
SHCP = Pin(27, mode=Mode.OUT)
STCP = Pin(4, mode=Mode.OUT)

SHCP.low()
STCP.low()

print("Setting DS HIGH...")
DS.high()

time.sleep(5)

print("DS should be HIGH now.")
print("Measure 74HC595 pin 14 to GND.")

time.sleep(5)

DS.low()

print("DS LOW.")
time.sleep(2)

DS.close()
SHCP.close()
STCP.close()