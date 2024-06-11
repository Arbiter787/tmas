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

def calibrate(voltage):
    try:
        file = open("ph_calibration.txt", 'w')
    except:
        print("Error opening ph_calibration.txt")
        quit()

    if voltage > 1322 and voltage < 1678:
        print("7.0 pH buffer solution detected")
        file.write("neutralVoltage=" + str(voltage) + '\n')
        #lines = file.readlines()
        #lines[0] = 'neutralVoltage=' + str(voltage) + '\n'
        
        #file.writelines(lines)
        print("pH 7.0 calibration complete")
    elif voltage > 1854 and voltage < 2210:
        print("4.0 pH buffer solution detected")
        file.write("acidVoltage=" + str(voltage))
        #lines = file.readlines()
        #lines[1] = 'acidVoltage=' + str(voltage) + '\n'
        
        #file.writelines(lines)
        print("pH 4.0 calibration complete")
    else:
        print("no calibration solution detected")

    file.close()

def reset():
    try:
        file = open("ph_calibration.txt", 'w')
    except:
        print("Error opening ph_calibration.txt")
        quit()
    
    neutralVoltage = 1500.0
    acidVoltage = 2032.44

    file.write("neutralVoltage=" + str(neutralVoltage) + '\n')
    file.write("acidVoltage=" + str(acidVoltage))
    file.close()

    print("Calibration reset to default.")

    
if __name__ == "__main__":
    while(True):
        print("Enter 'c' when the probe is placed within 4.0 or 7.0 pH calibration solution.\nPress Ctrl-C to quit calibration.")
        print("Enter 'r' to reset calibration to default.")
        command = input("Enter command: ")
        if command == 'c':
            calibrate(chan1.voltage * 1000)
        elif command == 'r':
            reset()
        else:
            print("Please enter a valid command.")