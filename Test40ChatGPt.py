'''This test is taking the data pin high as part of GPIO testing'''


import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(4, GPIO.OUT, initial=GPIO.LOW)

print("Clocking 8 times...")

for i in range(8):
    GPIO.output(22, GPIO.HIGH)
    time.sleep(0.3)
    GPIO.output(22, GPIO.LOW)
    time.sleep(0.3)

print("Done clocking.")
time.sleep(2)

print("Now latch HIGH")
GPIO.output(4, GPIO.HIGH)
time.sleep(2)

print("Now latch LOW")
GPIO.output(4, GPIO.LOW)

time.sleep(5)
GPIO.cleanup()