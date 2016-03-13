#!/usr/bin/env python3

# Partial re-write of the text_plugin made by Minorias
# to be compatible with any plugins.
# This version is much more simpler as it only allows to add text
# to an image

from image import Image

class Font:
    def __init__(self, font_file):
        self.font_file = '../fonts/' + font_file + '.txt'
        self.font = {} # Image array
        self.load_font()

    def load_font(self):
        file = open(self.font_file, 'r')
        raw_font = file.readlines()
        for i in range(len(raw_font)):
            if '--' in raw_font[i]:
                symbol = raw_font[i][2:].strip('\n')
            else:
                if symbol not in self.font.keys():
                    self.font[symbol] = []
                    self.font[symbol].append([raw_font[i].strip('\n')])
                else:
                    self.font[symbol].append([raw_font[i].strip('\n')])

    def char(self, char):
        return self.font[char]

class Text:
    def __init__(self, text, spacing=1, font_file='font'):
        self.text = text
        self.spacing = spacing

if __name__ == '__main__':
    lol = Font('font')
    print(lol.char('A'))