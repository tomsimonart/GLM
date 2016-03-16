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
        file = open(self.font_file, 'r')
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
    def __init__(self, text, spacing=1, font_file='font'):
        self.font_file = font_file
        self.spacing = spacing
        if len(text) <= 0:
            text = ' '
        font = Font(font_file)
        width = self.gen_width(text, font)+len(text)*spacing-spacing
        height = self.gen_height(text, font)
        Image.__init__(self, height=height,width=width)
        self.print(text, spacing, font)

    def gen_width(self, text, font):
        current_width = []
        width = []
        for i in text:
            for j in font.char(i).get_pixmap():
                current_width.append(len(j))
            width.append(max(current_width))
            current_width = []
        return sum(width)

    def gen_height(self, text, font):
        height = [max([len(font.char(i).get_pixmap()) for i in text])]
        return max(height)

    def print(self, text, spacing, font):
        cursor = 0
        for letter in text:
            self.paste(
                font.char(letter), x=cursor, y=0, mode='fill'
                )
            print(font.char(letter).get_pixmap())
            cursor += len(font.char(letter).get_pixmap()[0]) + spacing

if __name__ == '__main__':
    pass
    #from streamtools import Stream
    #streamer = Stream(matrix=True)
    #im = Image()
    
    #while True:
    #    entry = input('Text: ')
    #    text = Text(entry.lower())
    #    im.blank()
    #    im.paste(text.get_text(),x=0,y=5)
    #    streamer.set_data_from_matrix(im.get_pixmap())
    #    streamer.send_to_serial()
    #    print(streamer)