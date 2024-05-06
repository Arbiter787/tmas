import time
from pylibftdi import Device, Driver

# Custom class for interacting with Atlas Scientific sensors using FTDI
class AtlasDevice(Device):
    # Initialization with serial number to identify the specific FTDI device
    def __init__(self, sn):
        super().__init__(mode='t', device_id=sn)

    # Read a single line from the sensor, using "\r" as the line terminator
    def read_line(self, size=0):
        lsl = len('\r')
        line_buffer = []
        while True:
            next_char = self.read(1)
            if next_char == '' or (size > 0 and len(line_buffer) > size):
                break
            line_buffer.append(next_char)
            if (len(line_buffer) >= lsl and line_buffer[-lsl:] == list('\r')):
                break
        return ''.join(line_buffer)
    
    # Read multiple lines from the sensor, useful for commands that return multi-line responses
    def read_lines(self):
        lines = []
        try:
            while True:
                line = self.read_line()
                if not line:
                    break
                self.flush_input()  # Clear the input buffer to prepare for the next read
                lines.append(line)
            return lines
        
        except FtdiError:
            print("Failed to read from the sensor.")
            return ''        

    # Send a command to the sensor, ensuring it ends with a carriage return ("\r")
    def send_cmd(self, cmd):
        buf = cmd + "\r"
        try:
            self.write(buf)
            return True
        except FtdiError:
            print("Failed to send command to the sensor.")
            return False

# List all connected FTDI devices to help identify the pH sensor
def get_ftdi_device_list():
    dev_list = []
    for device in Driver().list_devices():
        # Decode device info from bytes to strings
        dev_info = map(lambda x: x.decode('latin1'), device)
        vendor, product, serial = dev_info
        dev_list.append(serial)
    return dev_list

if __name__ == '__main__':
    devices = get_ftdi_device_list()
    if devices:
        # Assume the first detected FTDI device is the pH sensor
        ph_device = AtlasDevice(devices[0])
        ph_device.send_cmd("C,0")  # Turn off continuous mode, if it's on
        time.sleep(1)
        ph_device.flush()

        while True:
            ph_device.send_cmd("R")  # Request a single reading
            time.sleep(1.5)  # Wait for the sensor to respond
            lines = ph_device.read_lines()
            for line in lines:
                # Filter out the command echo and empty lines
                if line.strip() and line.strip() != '*OK\r':
                    print("pH: ", line.strip())
            time.sleep(30)  # Wait for 30 seconds before requesting the next reading
    else:
        print("No FTDI devices found.")
