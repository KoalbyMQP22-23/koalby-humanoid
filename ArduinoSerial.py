#!/usr/bin/env python3
import time

import serial

'''
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
'''


class ArduinoSerial(object):

    def __init__(self):
        self.ser = serial.Serial('COM4', 115200, timeout=1)
        self.ser.reset_input_buffer()
        time.sleep(3)  # serial buffer needs 3 second delay before reading or writing
        # time.sleep sets serial to 0, DO NOT use 0 as a command on arduino side

    def send_command(self, command):  # sends a command to the arduino from the RasPi
        message = str.encode(command + '\r\n')
        self.ser.write(message)

    def read_command(self):  # reads a command to the arduino from the RasPi
        #   ser2 = serial.Serial('/dev/tty.usbmodem14201', 115200, timeout=1)
        line = self.ser.readline().decode('utf-8').strip()
        return line
