# Import Libraries
import os
import glob
import time
import requests


# Finds the correct device file that holds the temperature data
base_dir = '/sys/bus/w1/devices/'
try:
	device_folder = glob.glob(base_dir + '28*')[0]
except:
	print('')
	quit()

device_file = device_folder + '/w1_slave'

# A function that reads the sensors data
def read_temp_raw():
	f = open(device_file, 'r') # Opens the temperature device file
	lines = f.readlines() # Returns the text
	f.close()
	return lines

# Convert the value of the sensor into a temperature
def read():
	try:	
		lines = read_temp_raw() # Read the temperature 'device file'

		# While the first line does not contain 'YES', wait for 0.2s
		# and then read the device file again.
		while lines[0].strip()[-3:] != 'YES':
			time.sleep(0.2)
			lines = read_temp_raw()

		# Look for the position of the '=' in the second line of the
		# device file.
		equals_pos = lines[1].find('t=')

		# If the '=' is found, convert the rest of the line after the
		# '=' into degrees Celsius, then degrees Fahrenheit
		if equals_pos != -1:
			temp_string = lines[1][equals_pos+2:]
			temp_c = float(temp_string) / 1000.0
			return temp_c
	except:
		print('')
		quit()

if __name__ == '__main__':
				temp = read()
				print("Water_Temp {:.2f}".format(temp))
