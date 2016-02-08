#!/usr/bin/env python3

from os import system
from time import sleep
from stream_utils.streamtools import Stream

class ExamplePlugin(Stream):
    def __init__(self):
        # Credits - Version
        self.name = 'Demo Plugin'
        self.author = 'Infected'
        self.version = 'beta 0.4'

        # Stream initialization
        Stream.__init__(self, height=16, width=64)

        # Stream data
        self.data1 = ''.join([str((i+1)%2) for i in range(1024)])
        self.data2 = ''.join([str(i%2) for i in range(1024)])
        self.buffer_end = 0
        self.delay = 0.4

        # First data assignation (not necessary)
        Stream.set_data_from_string(self, self.data2)

    def stream(self):
        """Used to send the data to a Stream object
        stream(self) is the main loop of a plugin"""
        while self.buffer_end == 0:
            try:
                Stream.set_data_from_raw(self, self.data1)
                print(self, end='')
                Stream.send_to_serial(self)
                sleep(self.delay)
                system('clear')

                Stream.set_data_from_raw(self, self.data2)
                print(self, end='')
                Stream.send_to_serial(self)
                sleep(self.delay)
                system('clear')
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
plugin.stream()
plugin.get_info()
