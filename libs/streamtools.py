#!/usr/bin/env python3
# StreamTools by Infected

from serial import Serial
from time import sleep

class Stream():

    def __init__(self, matrix=True):
        self.matrix = matrix
        self.byte = bytes(1)
        self.lenght = 1024
        # Empty initial data
        self.data = ''.join(['0' for i in range(1024)])
        self.tty = '/dev/ttyACM0'
        self.baud_rate = 19200
        self.bytes_written = 0
        if self.matrix:
            self.arduino = Serial(self.tty, self.baud_rate)
            sleep(2)

    def __str__(self):
        display = ''
        if self.data != None:
            n = 0
            for i in range(16):
                for j in range(64):
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
        return 'Stream()'

    def __bytes__(self):
        byte_list = [int(self.data[i:i+8],2)for i in range(0,self.lenght-1,8)]
        return bytes(byte_list)

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
        if not self.matrix:
            return 0
        for i in range(0,self.lenght-1,8):
            try:
                self.arduino.write(int(self.data[i:i+8],2).to_bytes(1,'little'))
                #sleep(0.001)
                self.bytes_written += 1
                #print(self.bytes_written)
            except KeyboardInterrupt:
                # TO CORRECT
                for j in range(i, self.lenght-1,8):
                    self.arduino.write(int(0).to_bytes(1, 'little'))
                    sleep(0.001)
                sleep(0.02)
                print('Stream ended')
                exit()
        self.bytes_written = 0
        #exit()


    def __del__(self):
        pass