'''This is another version of holding data pin high and testing GPIO'''


import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

CLOCK = 17
LATCH = 4

GPIO.setup(CLOCK, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LATCH, GPIO.OUT, initial=GPIO.LOW)

print("Clocking...")

for i in range(8):
    GPIO.output(CLOCK, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(CLOCK, GPIO.LOW)
    time.sleep(0.5)

print("Eight clocks complete.")
time.sleep(2)

print("Latching...")
GPIO.output(LATCH, GPIO.HIGH)
time.sleep(1)
GPIO.output(LATCH, GPIO.LOW)

print("Done.")
time.sleep(5)

GPIO.cleanup()