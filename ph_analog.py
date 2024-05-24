# Luke Myers
# 5/23/2024
# Uses information from the DF Robot PH sensor sample code, available here:
# https://github.com/DFRobot/DFRobot_PH

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

adc_max = 43520
adc_min = 32700

# Create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# Create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# Create the mcp object
mcp = MCP.MCP3008(spi, cs)

# Create an analog input channel on pin 1
chan1 = AnalogIn(mcp, MCP.P1)

neutral_voltage = 1500.0
acid_voltage = 2032.44

# load calibration data from ph_calibration.txt
def load_calibration():
    try:
        file = open("ph_calibration.txt", 'r')
    except:
        print("PH -999")   # Error -999 - error loading calibration
        quit()
    
    neutral_voltage_line = file.readline()
    neutral_voltage_line = neutral_voltage_line.strip('neutralVoltage=')
    neutral_voltage = float(neutral_voltage_line)

    acid_voltage_line = file.readline()
    acid_voltage_line = acid_voltage_line.strip('acidVoltage=')
    acid_voltage = float(acid_voltage_line)

    return neutral_voltage, acid_voltage

# read voltage info
def read(voltage):
    neutral_voltage, acid_voltage = load_calibration()
    slope = (7.0 - 4.0) / ((neutral_voltage - 1500.0) / 3.0 - (acid_voltage - 1500.00) / 3.0)
    intercept = 7.0 - slope * (neutral_voltage - 1500.00) / 3.0
    ph_value = slope * (voltage - 1500.00) / 3.0 + intercept
    round(ph_value, 3)
    return ph_value

if __name__ == "__main__":
    ph = read(chan1.voltage)
    print("PH", ph)