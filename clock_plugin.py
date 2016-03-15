#!/usr/bin/env python3

from libs.streamtools import Stream
from libs.text import Text
from libs.image import Image
from datetime import datetime
from os import system
from time import sleep

class ClockPlugin:
    def __init__(self):
        self.author = 'Infected'
        self.name = 'Clock Plugin'
        self.version = 'V2.0'
        self.time = datetime.now()
        self.image = Image()
        self.canvas = Image()
        self.streamer = Stream(matrix=True)
        self.gen_canvas()

    def get_info(self):
        """Get the current state and information of the plugin"""
        print(self.name, self.author, self.version, sep='\n')

    def gen_canvas(self):
        self.canvas.draw_line(0, 0, 63, 0)
        self.canvas.draw_line(0, 0, 0, 15)
        self.canvas.draw_line(0, 15, 63, 15)
        self.canvas.draw_line(63, 0, 63, 15)

    def refresh(self):
        self.time = datetime.now()

    def print_time(self):
        self.timer = Text('{}:{}:{}'.format(
            str(self.time.hour).zfill(2),
            str(self.time.minute).zfill(2),
            str(self.time.second).zfill(2)), font_file='fontbignum')
        self.image.paste(self.timer.get_text(), x=3, y=3)
        self.image.paste(self.canvas.get_pixmap())

    def stream(self):
        self.image.blank()
        self.refresh()
        self.print_time()
        self.streamer.set_data_from_matrix(self.image.get_pixmap())
        self.streamer.send_to_serial()
        #print(self.streamer)

if __name__ == '__main__':
    plugin = ClockPlugin()
    plugin.get_info()
    while True:
        #system('clear')
        plugin.stream()
        #sleep(0.2)
