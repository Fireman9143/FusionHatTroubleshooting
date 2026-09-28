'''This is another attempt to swap GPIO pins and test signals'''


import RPi.GPIO as GPIO
import time

SDI = 17
SRCLK = 22
RCLK = 4

GPIO.setmode(GPIO.BCM)

GPIO.setup(SDI, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(SRCLK, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RCLK, GPIO.OUT, initial=GPIO.LOW)

# Shift 7 zeros
for _ in range(7):
    GPIO.output(SDI, GPIO.LOW)
    GPIO.output(SRCLK, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(SRCLK, GPIO.LOW)
    time.sleep(0.2)

# Shift one
GPIO.output(SDI, GPIO.HIGH)
time.sleep(0.2)

GPIO.output(SRCLK, GPIO.HIGH)
time.sleep(0.2)
GPIO.output(SRCLK, GPIO.LOW)

print("Eight bits shifted.")
time.sleep(2)

# Latch
GPIO.output(RCLK, GPIO.HIGH)
time.sleep(0.5)
GPIO.output(RCLK, GPIO.LOW)

print("Latched. Check pin 15.")
time.sleep(5)

GPIO.cleanup()