#!/usr/bin/python

# Made with heavy reference from the Atlas Scientific sample UART sensor code.

import serial
import time
import string
from serial import SerialException

# sends string command to sensor on serial. returns True if command was successfully sent.
def send_command(serial: serial.Serial, command: string):
    buf = command + "\r"    # add carriage return
    try:
        serial.write(buf.encode('utf-8'))
        return True
    except SerialException as e:
        return "Error, " + e


# reads a line from serial.
def read_line(serial: serial.Serial):
    lsl = len(b'\r')
    line_buffer = []
    while True:
        next_char = serial.read(1)
        if next_char == b'':
            break
        line_buffer.append(next_char)
        if len(line_buffer) >= lsl and line_buffer[-lsl:] == [b'\r']:
            break
    return b''.join(line_buffer)


# reads multiple lines from serial.
def read_lines(serial: serial.Serial):
    lines = []
    try:
        while True:
            line = read_line(serial)
            if not line:
                break
                serial.flush_input()
            lines.append(line)
        return lines
    except SerialException as e:
        return "Error, " + e

# reads data from sensor on serial_port
def read_data(serial_port):
    try:
        ser = serial.Serial(serial_port, 9600, timeout=0)
    except SerialException as e:
        return "Error, " + e
    
    cmd_result = send_command(ser, "R")
    if cmd_result != True:
        return cmd_result

    time.sleep(1.3)
    lines = read_lines(ser)
    if type(lines) == string:
        return lines
    for i in range(len(lines)):
        print(lines[i])
        lines[i] = lines[i].decode('utf-8')
        if lines[i][-1] == "\r":
            lines[i] = lines[i][:-1]      # strip carriage return
    
    data = lines[0]
    if lines[1] != "*OK":
        return "Error, sensor error with status " + lines[1] + " Reported reading " + data
    else:
        return data