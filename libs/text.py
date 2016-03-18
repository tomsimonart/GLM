#!/usr/bin/env python3

# Partial re-write of the text_plugin made by Minorias
# to be a lib instead of a plugin
# This version is much more simpler as it only allows to add text
# to an image

from libs.image import Image

class Font:
    def __init__(self, font_file='font', whitespace=1):
        self.font_file = './fonts/' + font_file + '.txt'
        self.whitespace = whitespace
        self.font = {} # Image array
        self.load_font()

    def load_font(self):
        file = open(self.font_file)
        raw_font = file.readlines()
        for i in range(len(raw_font)):
            if '--' in raw_font[i]:
                symbol = raw_font[i][2:].strip('\n')
            else:
                if symbol not in self.font.keys():
                    self.font[symbol] = []
                    self.font[symbol].append(
                        list(map(int, raw_font[i].strip('\n')))
                        )
                else:
                    self.font[symbol].append(
                        list(map(int, raw_font[i].strip('\n')))
                        )
        self.font[' '] = [[0] * self.whitespace]

    def char(self, char):
        if char not in self.font.keys():
            raise Exception('Font: character not found error [{}]'.format(char))
        return Image(pixmap=self.font[char])

class Text(Image):
    DEFAULT_FONT='font'
    def __init__(self, text='', spacing=1, font=None):
        super(Image, self).__init__()
        self.edit(text, spacing, font)

    def generate(self):
        self.width = \
            self.gen_width() + len(self.text) * self.spacing - self.spacing
        self.height = self.gen_height()
        self.blank()
        self.print()

    def edit(self, text, spacing=1, font=None):
        self.spacing = spacing
        self.text = text.strip('\n')
        if self.text == '':
            self.text = ' '
        if font == None:
            font = Text.DEFAULT_FONT
        self.edit_font(font)
        self.generate()

    def edit_font(self, font=None):
        if font == None:
            font = Text.DEFAULT_FONT
        self.font = Font(font)

    def gen_width(self):
        current_width = []
        width = []
        for i in self.text:
            for j in self.font.char(i).get_pixmap():
                current_width.append(len(j))
            width.append(max(current_width))
            current_width = []
        return sum(width)

    def gen_height(self):
        height = [
            max([len(self.font.char(i).get_pixmap()) for i in self.text])
            ]
        return max(height)

    def print(self):
        cursor = 0
        for letter in self.text:
            self.paste(
                self.font.char(letter), x=cursor, y=0, mode='fill'
                )
            cursor += len(
                self.font.char(letter).get_pixmap()[0]
                ) + self.spacing

    def get_pixmap(self):
        self.generate()
        self.print()
        return self.pixmap

if __name__ == '__main__':
    pass