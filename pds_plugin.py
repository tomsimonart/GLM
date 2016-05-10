#!/usr/bin/env python3

from libs.streamtools import Stream
from libs.image import Image
from random import randint
from time import sleep
from os import system

class Mouche:
    def __init__(self, min_x=0, min_y=0, max_x=64, max_y=16):
        self.max_x = max_x
        self.max_y = max_y
        self.min_x = min_x
        self.min_y = min_y
        self.x = (self.min_x + self.max_x) // 2
        self.y = (self.min_y + self.max_y) // 2
        self.trail_x = self.x
        self.trail_y = self.y
        self.previous = 1
        self.invert = {0:2,1:3,2:0,3:1}

    def casse_toi(self):
        self.trail_x = self.x
        self.trail_y = self.y
        direction = self.invert[self.previous]
        while direction == self.invert[self.previous]:
            direction = randint(0, 3)
        if direction == 0:
            self.add_x()
        elif direction == 1:
            self.add_y()
        elif direction == 2:
            self.dec_x()
        elif direction == 3:
            self.dec_y()
        self.previous = direction


    def add_x(self):
        self.x = self.x + 1 if self.x + 1 < self.max_x else self.x
    def add_y(self):
        self.y = self.y + 1 if self.y + 1 < self.max_y else self.y
    def dec_x(self):
        self.x = self.x - 1 if self.x - 1 >= self.min_x else self.x
    def dec_y(self):
        self.y = self.y - 1 if self.y - 1 >= self.min_y else self.y

    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_trail_x(self):
        return self.trail_x
    def get_trail_y(self):
        return self.trail_y


class PdsPlugin:
    def __init__(self, matrix=True, delay=0.2):
        self.matrix = matrix
        self.author = 'Infected'
        self.name = 'PDS Plugin'
        self.version = '0.1a'

        self.image = Image()
        self.monitor = Stream(matrix=self.matrix)
        self.delay = float(delay)

    def get_info(self):
        """Get the current state and information of the plugin"""
        print(self.name, self.author, self.version, sep='\n')

    def get_delay(self):
        return self.delay

    def get_image(self):
        return self.image

    def set_pixmap(self, image):
        self.image.set_pixmap(image)

    def get_pixmap(self):
        return self.image.get_pixmap()

    def stream(self):
        self.monitor.set_data_from_matrix(self.get_pixmap())
        #system('clear')
        #print(self.monitor)
        if self.matrix:
            self.monitor.send_to_serial()

    def blank(self):
        self.image.blank()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-n',
        '--no-matrix',
        dest="no_matrix",
        default=False,
        action="store_true",
        help="Don't connect to any arduino"
        )
    parser.add_argument(
        '-d',
        '--delay',
        dest='delay',
        help='refresh rate',
        default=0.2
        )
    parser.add_argument(
        '-m',
        '--mouches',
        dest='mouches',
        help='nombre de mouches',
        default=1,
        )
    args = parser.parse_args()

    if args.no_matrix:
        mode = False
    else:
        mode = True

    plugin = PdsPlugin(matrix=mode, delay=args.delay)
    plugin.get_info()
    mouches = []
    for i in range(int(args.mouches)):
        mouches.append(Mouche())
    while True:
        try:
            plugin.stream()
            plugin.blank()
            sleep(plugin.get_delay())

            new_pixmap = plugin.get_pixmap()
            for mouche in mouches:
                new_pixmap[mouche.get_y()][mouche.get_x()] = 1
                new_pixmap[mouche.get_trail_y()][mouche.get_trail_x()] = 1

            plugin.set_pixmap(new_pixmap)
            for mouche in mouches:
                mouche.casse_toi()

        except KeyboardInterrupt:
            print('END')
            exit()
