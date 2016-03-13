#!/usr/bin/env python3
from libs.streamtools import Stream
from libs import pbmtools

class PbmPlugin(Stream):
    def __init__(self, file_in='test', directory='./pbm'):
        self.author = 'Infected'
        self.name = 'Pbm Plugin'
        self.version = '1.0'

        self.mime = '.pbm'
        self.selection = None
        self.directory = directory + '/'
        # File name
        self.file_in = self.directory + file_in + self.mime
        self.file_tmp = self.directory + 'pbm.tmp'
        # Opened file
        self.pbm_in = None
        self.pbm_data = None

        self.END = 'exit'

        Stream.__init__(self)

    def prompt(self):
        self.selection = input('>>> ')
        return self.selection

    def get_selection(self):
        return self.selection

    def stream(self):
        self.set_file_in(self.selection)
        self.clean_pbm()
        self.load_pbm_in()
        self.load_pbm_data()
        if self.pbm_in != None and self.pbm_data != None:
            Stream.set_data_from_string(self, self.pbm_data)
            # Stream.send_to_serial(self)
            self.pbm_in.close()

    def load_pbm_data(self):
        try:
            data = open(self.file_tmp)
            self.pbm_data = ''.join(
                [i.ljust(64,'0') for i in data.read().split('\n')]
                )
            if len(self.pbm_data) < 1024:
                self.pbm_data += '0' * (1024 - len(self.pbm_data))
            data.close()
        except FileNotFoundError:
            data = None
            self.pbm_data = None

    def clean_pbm(self):
        pbmtools.clean_pbm(self.file_in, self.file_tmp)

    def load_pbm_in(self):
        try:
            self.pbm_in = open(self.file_in, mode='r')
        except FileNotFoundError:
            self.pbm_in = None

    def set_file_in(self, file_in):
        self.file_in = self.directory + file_in + self.mime

    def set_directory(self, directory):
        self.directory = directory

    def get_directory(self):
        return self.directory

    def __del__(self):
        pass

if __name__ == '__main__':
    import os

    plugin = PbmPlugin()
    while plugin.prompt() != plugin.END:
        if plugin.get_selection() == 'ls':
            os.system('ls ' + plugin.directory + ' | grep --color=auto .pbm')
        else:
            plugin.stream()
            print(plugin, end='')
            # print(bytes(plugin))
            plugin.send_to_serial()
