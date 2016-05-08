#!/usr/bin/env python3
# StreamTools by Infected

from .rainbow import msg
from serial import Serial
from time import sleep

MAT_WIDTH = 64
MAT_HEIGHT = 16


class Stream:
    def __init__(self, matrix=True, tty="/dev/ttyACM0"):
        self.matrix = matrix
        self.byte = bytes(1)
        self.lenght = 1024
        # Empty initial data
        self.data = ''.join(['0' for i in range(1024)])
        self.tty = tty
        self.__baud_rate = 19200
        self.bytes_written = 0
        if self.matrix:
            self.arduino = Serial(self.tty, self.__baud_rate)
            sleep(2)

    def __str__(self):
        display = ''
        if self.data is not None:
            n = 0
            for i in range(MAT_HEIGHT):
                for j in range(MAT_WIDTH):
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
        byte_list = [
            int(self.data[i:i+8], 2)for i in range(0, self.lenght-1, 8)]
        return bytes(byte_list)

    def set_data(self, data):
        if not hasattr(data, 'get_pixmap'):
            msg("set_data()", "not an Image", 1)
            return None
        else:
            if data.height != MAT_HEIGHT or data.width != MAT_WIDTH:
                msg(
                    "Image size doesn't match matrix size",
                    3,
                    "Stream.set_data")
                exit()
            else:
                self.set_data_from_matrix(data.get_pixmap())

    def set_data_from_raw(self, data):
        msg("this function is deprecated", 1, "Stream.set_data_from_matrix")
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
        for i in range(0, self.lenght-1, 8):
            try:
                self.arduino.write(
                    int(self.data[i:i+8], 2).to_bytes(1, 'little'))
                self.bytes_written += 1
            except KeyboardInterrupt:
                for j in range(i, self.lenght-1, 8):
                    self.arduino.write(int(0).to_bytes(1, 'little'))
                    sleep(0.001)
                sleep(0.02)
                print('Stream ended')
                exit()
        self.bytes_written = 0
