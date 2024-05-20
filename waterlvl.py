import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
import sys
from adafruit_mcp3xxx.analog_in import AnalogIn

adc_max = 43520
adc_min = 32700

# Create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# Create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# Create the mcp object
mcp = MCP.MCP3008(spi, cs)

# Create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P0)

raw_adc = (chan0.value)

if (raw_adc == 0) or (raw_adc < (0.75 * adc_min)) or (raw_adc > 60000):
	print('')
	quit()
else:
	if (raw_adc > adc_max):
		raw_adc = adc_max

	percentage = 1 - ((raw_adc - adc_min) * 1) / (adc_max - adc_min)

	if (percentage < 0):
		percentage = 0

	print('Water_Level', (1 + round(percentage * 4, 1)))