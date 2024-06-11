# Import Libraries
import os
import glob
import time
import requests


# Finds the correct device file that holds the temperature data
def find_device(base_dir):
	try:
		device_folder = glob.glob(base_dir + '28*')[0]
		return device_folder
	except:
		print('Water_Temp -999')    # Error code 999 = Error finding device
		quit()

# A function that reads the sensors data
def read_temp_raw(device_file):
	try:
		f = open(device_file, 'r') # Opens the temperature device file
	except OSError:
		return('-998')   # Error code 998 = Error opening device file
	lines = f.readlines() # Returns the text
	f.close()
	return lines

# Convert the value of the sensor into a temperature
def read(device_file):
	try:	
		lines = read_temp_raw(device_file) # Read the temperature 'device file'

		# While the first line does not contain 'YES', wait for 0.2s
		# and then read the device file again.
		count = 0
		while lines[0].strip()[-3:] != 'YES':
			time.sleep(0.2)
			count += 1
			lines = read_temp_raw(device_file)

			if count > 1000:     # prevent infinite loops
				return(-997)

		# Look for the position of the '=' in the second line of the
		# device file.
		equals_pos = lines[1].find('t=')

		if equals_pos == -1:
			return(-997)   # Error code 997: Error reading from device
		
		# If the '=' is found, convert the rest of the line after the
		# '=' into degrees Celsius, then degrees Fahrenheit
		if equals_pos != -1:
			temp_string = lines[1][equals_pos+2:]
			temp_c = float(temp_string) / 1000.0
			return temp_c
	except:
		return(-997)    # Error code 997: Error reading from device

if __name__ == '__main__':
	dir = '/sys/bus/w1/devices/'
	folder = find_device(dir)
	file = folder + '/w1_slave'
	temp = read(file)
	print("Water_Temp {:.2f}".format(temp))
