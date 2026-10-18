# Temperature and humidity with the DHT11 sensor
#
# This program asks the sensor for the temperature and humidity
# every 2 seconds and prints the answer on the screen.
# Press Ctrl+C to stop it.

from time import sleep

# ---- Setup for the Raspberry Pi 5 (you can skip these 3 lines) ----
from gpiozero import Device
from gpiozero.pins.lgpio import LGPIOFactory
Device.pin_factory = LGPIOFactory(chip=15)
# --------------------------------------------------------------------

from fusion_hat.modules import DHT11

# The sensor's data wire is plugged into GPIO pin 5.
# Change this number if you plug it into a different pin.
dht11 = DHT11(pin=5)

while True:
    result = dht11.read()   # Ask the sensor for a reading

    # A good reading has a humidity bigger than 0.
    # A humidity of 0 is impossible, so it means the sensor failed this time.
    if result and result[0] > 0:
        humidity, temperature = result
        fahrenheit = temperature * 9 / 5 + 32
        print(f"Humidity: {humidity}%")
        print(f"Temperature: {temperature} C  or  {round(fahrenheit, 1)} F")
        print()
    else:
        print("Bad reading. Trying again...")

    sleep(2)   # Wait 2 seconds before asking again