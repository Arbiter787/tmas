# Luke Myers
# 5/23/2024
# Uses information from the DF Robot EC sensor sample code, available here:
# https://github.com/DFRobot/DFRobot_PH

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import temp

# Create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# Create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# Create the mcp object
mcp = MCP.MCP3008(spi, cs)

# Create an analog input channel on pin 1
chan1 = AnalogIn(mcp, MCP.P1)

low_k = 1.0
high_k = 1.0

# load calibration data from salinity_calibration.txt
def load_calibration():
    try:
        file = open("salinity_calibration.txt", 'r')
    except:
        print("Salinity -999")   # Error -999 - error loading calibration
        quit()
    
    low_k_line = file.readline()
    low_k_line = low_k_line.strip('kvalueLow=')
    low_k = float(low_k_line)

    high_k_line = file.readline()
    high_k_line = high_k_line.strip('kvalueHigh=')
    high_k = float(high_k_line)

    return low_k, high_k

# read voltage info and convert to salinity
def read(voltage, temperature):
    k_value = 1.0
    low_k, high_k = load_calibration()

    ec = 1000 * voltage / 820.0 / 200.0
    temp_value = ec * k_value

    if (temp_value > 2.5):
        k_value = high_k
    elif (temp_value < 2.0):
        k_value = low_k
    
    value = ec * value
    value = value / (1.0 + 0.0185 * (temperature - 25.0))

    return value

if __name__ == "__main__":

    temp_dir = '/sys/bus/w1/devices/'
    temp_folder = temp.find_device(temp_dir)
    temp_file = temp_folder + '/w1_slave'

    # temperature compensation
    temperature = temp.read(temp_file)
    if temperature == -997:
        salinity = read(chan1.voltage * 1000, 25.0)  # if sensor error, use default temp of 25C
    else:
        salinity = read(chan1.voltage * 1000, temperature)
    
    print("Salinity", salinity)