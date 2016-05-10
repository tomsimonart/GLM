#!/usr/bin/env python3

# Partial re-write of the text_plugin made by Minorias
# to be a lib instead of a plugin
# This version is much more simpler as it only allows to add text
# to an image

from libs.image import Image

FONT_DIR = "./fonts/"


class Font:
    def __init__(self, font_file='font', whitespace=1):
        self.font_file = FONT_DIR + font_file + '.txt'
        self.whitespace = whitespace
        self.font = {}  # Image array
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
            raise Exception(
                'Font: character not found error [{}]'.format(char)
                )
        return Image(pixmap=self.font[char])


class Text(Image):
    """
    A Text is an Image with characters pasted to it from a Font.

    Keyword arguments:
    text -- text to be written (default '')
    spacing -- spacing size between characters (default 1)
    font -- font file to be used from FONT_DIR (default None)
    """

    DEFAULT_FONT = 'font'

    def __init__(self, text='', spacing=1, font=None):
        super(Image, self).__init__()
        self.edit(text, spacing, font)

    def generate(self):
        """
        Blank the Text and paste all letters on it
        """
        self.width = \
            self.gen_width() + len(self.text) * self.spacing - self.spacing
        self.height = self.gen_height()
        self.blank()
        self.print_letter()

    def edit(self, text='', spacing=1, font=None):
        """
        Blank the current Text and generate a new one with "text".

        Keyword arguments:
        text -- text to be written (default '')
        spacing -- spacing size between characters (default 1)
        font -- font file to be used from FONT_DIR (default None)
        """
        self.spacing = spacing
        self.text = str(text).strip('\n')
        if self.text == '':
            self.text = ' '

        elif font is None:
            font = Text.DEFAULT_FONT

        if not hasattr(self, 'font'):  # Load font once
            self.edit_font(font)
        elif self.font.font_file != FONT_DIR + font + '.txt':
            self.edit_font(font)

        self.generate()

    def edit_font(self, font=None):
        if font is None:
            font = Text.DEFAULT_FONT
        self.font = Font(font)

    def gen_width(self) -> int:
        """Compute the width of a string"""
        current_width = []
        width = []
        for i in self.text:
            for j in self.font.char(i).get_pixmap():
                current_width.append(len(j))
            width.append(max(current_width))
            current_width = []
        return sum(width)

    def gen_height(self) -> int:
        """Compute the max height of characters in a string"""
        height = [
            max([len(self.font.char(i).get_pixmap()) for i in self.text])]
        return max(height)

    def print_letter(self):
        cursor = 0
        for letter in self.text:
            character = self.font.char(letter)
            self.paste(character, x=cursor, y=0, mode='fill')
            cursor += len(character.get_pixmap()[0]) + self.spacing
