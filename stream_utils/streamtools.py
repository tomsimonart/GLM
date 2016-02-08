#!/usr/bin/env python3
# StreamTools by Infected

from serial import Serial

class Stream():

    def __init__(self, height=16, width=64):
        self.height = height
        self.width = width
        self.lenght = height * width
        self.byte = bytes(1)
        # Empty initial data
        self.data = ''.join(['0' for i in range(self.height * self.width)])
        self.arduino = Serial('/dev/ttyACM0', 9600)

    def __str__(self):
        display = ''
        if self.data != None:
            n = 0
            for i in range(self.height):
                for j in range(self.width):
                    if self.data[n] == '1':
                        display += "\033[41m \033[0m"
                    else:
                        display += "\033[44m \033[0m"
                    n += 1
                display += '\n'
        else:
            display = 'StreamError: No data to display'
        return display

    def __repr__(self):
        return 'Stream(' + str(self.height) + ', ' + str(self.width) + ')'

    def __bytes__(self):
        byte_list = [int(self.data[i:i+8],2)for i in range(0,self.lenght-1,8)]
        return bytes(byte_list)

    def set_size(self, height, width):
        self.height = height
        self.width = width

    def set_height(self, height):
        self.height = height

    def set_width(self, width):
        self.width = width

    def set_data_from_raw(self, data):
        """Fastest solution if the data is in a stripped string format"""
        self.data = data

    def set_data_from_matrix(self, data):
        matrix = ''.join([str(j) for i in data for j in i])
        self.data = matrix

    def set_data_from_string(self, data):
        self.data = data.replace('\n', '').strip()

    def set_data_from_list(self, data):
        self.data = ''.join(map(str, data))

    def get_data(self):
        return self.data

    def send_to_serial(self):
        for i in range(0,self.lenght-1,8):
            self.arduino.write(int(self.data[i:i+8],2).to_bytes(1,'little'))

    def refresh(self):
        self.lenght = self.height * self.width

    def __del__(self):
        pass