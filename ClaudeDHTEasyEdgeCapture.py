# Temperature and humidity with the DHT11 sensor - the "listen to the wire" way
#
# How the sensor talks:
#   1. We pull the wire LOW for a moment. That means "please send a reading!"
#   2. The sensor answers with 40 pulses (short beeps on the wire).
#        A SHORT pulse means 0.     A LONG pulse means 1.
#   3. The 40 bits make 5 numbers: humidity, humidity decimal,
#      temperature, temperature decimal, and a "checksum" that lets us
#      check that nothing got mixed up on the way.
#
# The Raspberry Pi writes down the exact time of every change on the wire,
# so we can measure how long each pulse is.
#
# Press Ctrl+C to stop the program.

import lgpio
from time import sleep

CHIP_NUMBER = 15   # Which GPIO chip the Raspberry Pi 5 uses
PIN = 5            # The sensor's data wire is plugged into GPIO pin 5

edges = []         # Every change on the wire gets saved in this list


def remember_edge(chip_id, gpio, level, timestamp):
    """The Pi calls this every time the wire changes. We save what happened."""
    # level 1 = the wire went UP (HIGH).  level 0 = it went DOWN (LOW).
    if level == 0 or level == 1:
        edges.append((level, timestamp))


def ask_sensor():
    """Send the start signal, then listen to the sensor's answer."""
    edges.clear()

    # Pull the wire LOW for 20 milliseconds. This means "send me a reading!"
    lgpio.gpio_free(chip, PIN)
    lgpio.gpio_claim_output(chip, PIN, 0)
    sleep(0.020)

    # Let go of the wire and listen. The answer takes about 5 milliseconds.
    lgpio.gpio_free(chip, PIN)
    lgpio.gpio_claim_alert(chip, PIN, lgpio.BOTH_EDGES, lgpio.SET_PULL_UP)
    sleep(0.010)

    return list(edges)


def find_pulse_lengths(changes):
    """Measure how long the wire stays HIGH each time (in microseconds)."""
    lengths = []
    for i in range(len(changes) - 1):
        level, start_time = changes[i]
        next_level, end_time = changes[i + 1]
        if level == 1 and next_level == 0:            # it went up, then back down
            lengths.append((end_time - start_time) / 1000)   # nanoseconds -> microseconds
    return lengths


def lengths_to_bits(lengths):
    """A short pulse (about 27) is a 0. A long pulse (about 70) is a 1."""
    bits = []
    for length in lengths:
        if length > 48:          # 48 is halfway between 27 and 70
            bits.append(1)
        else:
            bits.append(0)
    return bits


def bits_to_numbers(bits):
    """Group the 40 bits into 5 numbers, 8 bits each."""
    numbers = []
    for start in range(0, 40, 8):
        number = 0
        for bit in bits[start:start + 8]:
            number = number * 2 + bit      # slide the number over and add the next bit
        numbers.append(number)
    return numbers


def read_sensor():
    """Ask the sensor. Give back (humidity, temperature), or None if it went wrong."""
    lengths = find_pulse_lengths(ask_sensor())

    # We need 40 pulses. We use the LAST 40, because the first pulse
    # (the sensor saying hello) isn't part of the data.
    if len(lengths) < 40:
        return None
    bits = lengths_to_bits(lengths[-40:])
    humidity, humidity_decimal, temperature, temperature_decimal, checksum = bits_to_numbers(bits)

    # The checksum must equal the other four numbers added up.
    if (humidity + humidity_decimal + temperature + temperature_decimal) % 256 != checksum:
        return None

    # The decimal parts are always one digit (0 to 9).
    if humidity_decimal > 9 or temperature_decimal > 9:
        return None

    humidity = round(humidity + humidity_decimal / 10, 1)
    temperature = round(temperature + temperature_decimal / 10, 1)

    # The DHT11 only works from 0 to 50 degrees. Anything else is a mistake.
    if humidity < 1 or humidity > 100 or temperature < 0 or temperature > 50:
        return None

    return humidity, temperature


# ---- Start listening to the sensor's wire ----
chip = lgpio.gpiochip_open(CHIP_NUMBER)
lgpio.gpio_claim_alert(chip, PIN, lgpio.BOTH_EDGES, lgpio.SET_PULL_UP)
listener = lgpio.callback(chip, PIN, lgpio.BOTH_EDGES, remember_edge)

try:
    while True:
        reading = read_sensor()

        if reading:
            humidity, temperature = reading
            fahrenheit = temperature * 9 / 5 + 32
            print(f"Humidity: {humidity}%")
            print(f"Temperature: {temperature} C  or  {round(fahrenheit, 1)} F")
            print()
        else:
            print("Bad reading. Trying again...")

        sleep(2)   # The sensor needs a short rest between readings

except KeyboardInterrupt:
    print("Goodbye!")

finally:
    # Tidy up: give the pin back to the Pi
    listener.cancel()
    lgpio.gpio_free(chip, PIN)
    lgpio.gpiochip_close(chip)