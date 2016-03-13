#!/usr/bin/env python3

from os import system
from time import sleep
from libs.streamtools import Stream
from libs.image import Image

class ExamplePlugin(Image):
    def __init__(self):
        # Credits - Version
        self.name = 'Demo Plugin'
        self.author = 'Infected'
        self.version = 'beta 0.4'

        # Stream initialization
        Image.__init__(self)

        # Stream data
        self.data1 = [[0,1] * 8 for i in range(1024)]
        self.data2 = [[1,0] * 8 for i in range(1024)]
        self.buffer_end = 0
        self.delay = 0.5

    def stream(self):
        """Used to send the data to a Stream object
        stream(self) is the main loop of a plugin"""

        arduino = Stream()

        while self.buffer_end == 0:
            try:
                self.pixmap = self.data1
                arduino.set_data_from_matrix(self.pixmap)
                arduino.send_to_serial()
                sleep(self.delay)

                self.pixmap = self.data2
                arduino.set_data_from_matrix(self.pixmap)
                arduino.send_to_serial()
                sleep(self.delay)
            except KeyboardInterrupt:
                print('\nEnd')
                exit()

    def get_info(self):
        """Get the current state and information of the plugin"""
        print(self.name, self.author, self.version, sep='\n')
        print(self.__repr__())
        print(self,end='')
        print(bytes(self))

plugin = ExamplePlugin()
plugin.get_info()
plugin.stream()
