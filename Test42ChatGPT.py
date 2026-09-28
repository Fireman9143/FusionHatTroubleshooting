'''At this point in the testing, ChatGPT had me manually powering, clocking, and latching bits 
with just a chip on a breadboard.  No code, no fusion hat.  The chip cycled properly.  I also 
bought more 74HC595N chips and tested a new chip the same way.  When connecting back to the fusion
there were new errors of not initializing the GPIO.  Somehow the fusion hat was loading RPI.GPIO
from the global python library and not the venv, which was a different version.  After following 
instructions to remove the older version and install the newer version globally, the GPIO worked
again. Also because it was a new chip, I went back and setup and ran the original Sunfounder 1.8
display example and got the same behavior of losing segments each time the program ran.  Here is 
the original Sunfounder example with one change from AI commented in the code'''


#!/usr/bin/env python3
from fusion_hat.pin import Pin, Mode
import time
import threading

# Define GPIO pins for the 74HC595 shift register
SDI = Pin(17,mode=Mode.OUT)   # Serial Data Input
RCLK = Pin(4,mode=Mode.OUT)  # Register Clock
SRCLK = Pin(27,mode=Mode.OUT) # Shift Register Clock

# Define GPIO pins for digit selection on the 7-segment display
placePin = [Pin(pin,mode=Mode.OUT) for pin in (23, 24, 25, 12)]

# Define segment codes for numbers 0-9 for the 7-segment display
number = (0xc0, 0xf9, 0xa4, 0xb0, 0x99, 0x92, 0x82, 0xf8, 0x80, 0x90)

counter = 0  # Initialize counter for display
timer1 = 0   # Initialize timer for counter increment

def clearDisplay():
   """ Clear the 7-segment display. """
   for _ in range(8):
      SDI.high()
      SRCLK.high()
      SRCLK.low()
   RCLK.high()
   RCLK.low()

#AI opted for a different syntax to shift the bits.  It made no difference in the results.
def hc595_shift(data):
    for i in range(8):
        bit = 1 if (data & (0x80 >> i)) else 0
        SDI.value(bit)
        SRCLK.high()
        SRCLK.low()

    RCLK.high()
    RCLK.low()


# def hc595_shift(data):
#    """ Shift a byte of data to the 74HC595 shift register. """
#    for i in range(8):
#       SDI.value(0x80 & (data << i))  # Set SDI high/low based on data bit
#       SRCLK.high()  # Pulse the Shift Register Clock
#       SRCLK.low()
#    RCLK.high()  # Latch data on the output by pulsing Register Clock
#    RCLK.low()

def pickDigit(digit):
   """ Select a digit for display on the 7-segment display. """
   for pin in placePin:
      pin.low()  # Turn off all digit selection pins
   placePin[digit].high()  # Turn on the selected digit

def timer():
   """ Timer function to increment the counter every second. """
   global counter, timer1
   timer1 = threading.Timer(1.0, timer)  # Reset timer for next increment
   timer1.start()
   counter += 1  # Increment counter
   print("%d" % counter)  # Print current counter value

def setup():
   """ Setup initial state and start the timer. """
   global timer1
   timer1 = threading.Timer(1.0, timer)  # Initialize and start the timer
   timer1.start()

def loop():
   """ Main loop to update the 7-segment display with counter value. """
   global counter
   while True:
      for i in range(4):  # Loop through each digit
            clearDisplay()  # Clear display before setting new digit
            pickDigit(i)    # Select digit for display

            # Choose the digit of counter to display
            digit = (counter // (10 ** (3-i))) % 10

            hc595_shift(number[digit])  # Shift digit value to 74HC595
            time.sleep(0.001)  # Short delay for display stability

def destroy():
   """ Cleanup GPIO resources and stop timer on exit. """
   global timer1
   timer1.cancel()  # Stop the timer
   for device in [SDI, RCLK, SRCLK] + placePin:
      device.close()  # Close GPIO devices

try:
   setup()  # Initialize the setup
   while True:
      loop()  # Start the main loop

except KeyboardInterrupt:
   # Handle script interruption (e.g., Ctrl+C)
   destroy()  # Cleanup resources on exit