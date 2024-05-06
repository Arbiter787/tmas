import os
import glob
import time
import datetime
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from prometheus_client import start_http_server, Gauge

# Create metrics to track the temperature and water level
temperature_gauge = Gauge('water_temperature_celsius', 'Water temperature in Celsius')
water_level_gauge = Gauge('water_level', 'Water level (1-5)')

# Base directory for the temperature sensor
base_dir = '/sys/bus/w1/devices/'

try:
    device_folder = glob.glob(base_dir + '28*')[0]
except IndexError:
    print("Temperature sensor not found")
    quit()

device_file = device_folder + '/w1_slave'

# A function that reads the sensor's data
def read_temp_raw():
    with open(device_file, 'r') as f:  # Opens the temperature device file
        lines = f.readlines()  # Returns the text
    return lines

# Convert the value of the sensor into a temperature
def read_temp():
    try:
        lines = read_temp_raw()  # Read the temperature 'device file'
        # While the first line does not contain 'YES', wait for 0.2s and then read the device file again.
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        # Look for the position of the '=' in the second line of the device file.
        equals_pos = lines[1].find('t=')
        # If '=' is found, convert the rest of the line after the '=' into degrees Celsius
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c
    except:
        print("Error reading temperature")
        quit()

# Start up the server to expose the metrics.
start_http_server(8000)

# Water level sensor setup
adc_max = 42100
adc_min = 32700

# Create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# Create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# Create the mcp object
mcp = MCP.MCP3008(spi, cs)

# Create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P0)

def read_water_level():
    raw_adc = chan0.value

    if (raw_adc == 0) or (raw_adc < (0.75 * adc_min)) or (raw_adc > 60000):
        return None
    else:
        if (raw_adc > adc_max):
            raw_adc = adc_max

        percentage = 1 - ((raw_adc - adc_min) * 1) / (adc_max - adc_min)

        if (percentage < 0):
            percentage = 0

        return 1 + round(percentage * 4, 1)

if __name__ == '__main__':
    while True:
        temp = read_temp()
        temperature_gauge.set(temp)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
        print("+-----------------------------+")
        print(f"| {timestamp} |")
        print("| Water Temp: {:.2f}Â°C |".format(temp))

        water_level = read_water_level()
        if water_level is not None:
            water_level_gauge.set(water_level)
            print("| Water Level: {} |".format(water_level))

        print("+-----------------------------+")
        time.sleep(30)  # Wait for 30 seconds before the next reading
