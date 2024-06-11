# Luke Myers
# 5/28/2024
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

def calibrate(voltage, temperature):
    try:
        file = open("salinity_calibration.txt", 'r+')
    except:
        print("Error opening salinity_calibration.txt")
        quit()

    ec = 1000 * voltage / 820.0 / 200.0
    
    if ec > 0.9 and ec < 1.9:
        compensated_solution_ec = 1.413 * (1.0 + 0.0185 * (temperature - 25.0))
        temp_k = 820.0 * 200.0 * compensated_solution_ec / 1000.0 / voltage
        temp_k = round(temp_k, 2)

        print("1.413 ms/cm buffer solution detected")
        lines = file.readlines()
        lines[0] = 'kvalueLow=' + str(temp_k) + '\n'
        
        file.writelines(lines)
        print("1.413 ms/cm calibration complete")
    elif ec > 9.0 and ec < 16.8:
        compensated_solution_ec = 12.88 * (1.0 + 0.0185 * (temperature - 25.0))
        temp_k = 820.0 * 200.0 * compensated_solution_ec / 1000.0 / voltage
        temp_k = round(temp_k, 2)

        print("12.88 ms/cm buffer solution detected")
        lines = file.readlines()
        lines[1] = 'kvalueHigh=' + str(temp_k) + '\n'
        
        file.writelines(lines)
        print("12.88 ms/cm calibration complete")
    else:
        print("no calibration solution detected")

    file.close()

def reset():
    try:
        file = open("salinity_calibration.txt", 'w+')
    except:
        print("Error opening salinity_calibration.txt")
        quit()
    
    low_k = 1.0
    high_k = 1.0

    lines = file.readlines()
    lines[0] = 'kvalueLow=' + str(low_k) + '\n'
    lines[1] = 'kvalueHigh=' + str(high_k) + '\n'
    file.close()

    print("Calibration reset to default.")

    
if __name__ == "__main__":
    while(True):
        print("Enter 'c' when the probe is placed within 1.413 or 12.88 ms/cm calibration solution.\nPress Ctrl-C to quit calibration.")
        print("If this package has a temperature sensor, it will be used to compensate for temperature.\nPlease place the temperature sensor in the calibration solution as well.")
        print("Enter 'r' to reset calibration to default.")
        command = input("Enter command: ")
        if command == 'c':
            # temperature compensation
            temperature = temp.read()
            if temperature == -997:
                temperature = 25.0  # if sensor error, use default temp of 25C

            calibrate(chan1.voltage * 1000, temperature)
        elif command == 'r':
            reset()
        else:
            print("Please enter a valid command.")