#!/usr/bin/env python3
from datetime import datetime
from libs.screen import Screen
from libs.text import Text
from libs.image import Image
from libs.drawer import Drawer
from libs.rainbow import color, msg
from os import system
from time import sleep


class ClockPlugin:
    def __init__(self, matrix=False, show=False):
        self.author = 'Infected'
        self.name = 'Clock Plugin'
        self.version = '0.0.1'
        self.time = datetime.now()
        self.timer = Text()
        self.canvas = Image(64, 16)
        self.time_frame = Image(64, 16)
        self.canvas_draw = Drawer(self.canvas)
        self.invert = Image(64, 16)
        self.invert.fill()

        self.screen = Screen(matrix=matrix, show=show, fps=15)
        self.screen.add(self.time_frame, refresh=True)
        self.screen.add(self.timer, refresh=True, x=3, y=3)
        self.screen.add(self.canvas, refresh=False)
        self.screen.add(self.invert, mode='invert', refresh=False)

        self.gen_canvas()

    def get_info(self):
        """Get the current state and information of the plugin"""
        print(color(self.name, "red"),
              color(self.author, "green"),
              color(self.version, "magenta"),
              sep='\n')

    def gen_canvas(self):
        self.canvas_draw.line(0, 0, 63, 0)
        self.canvas_draw.line(0, 0, 0, 15)
        self.canvas_draw.line(0, 15, 63, 15)
        self.canvas_draw.line(63, 0, 63, 15)

    def refresh(self):
        self.time = datetime.now()

    def print_time(self):
        self.timer.edit('{}:{}:{}'.format(
            str(self.time.hour).zfill(2),
            str(self.time.minute).zfill(2),
            str(self.time.second).zfill(2)),
            font='fontbignum')

    def start(self):
        self.refresh()
        self.print_time()
        self.screen.refresh()


if __name__ == '__main__':
    plugin = ClockPlugin()
    plugin.get_info()
    input()
    while True:
        plugin.stream()
