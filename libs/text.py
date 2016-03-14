#!/usr/bin/env python3

# Partial re-write of the text_plugin made by Minorias
# to be a lib instead of a plugin
# This version is much more simpler as it only allows to add text
# to an image

from image import Image

class Font:
    def __init__(self, font_file='font', whitespace=1):
        self.font_file = '../fonts/' + font_file + '.txt'
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
            print('Font: character not found error [{}]'.format(char))
            exit()
        return self.font[char]

class Text:
    def __init__(self, text, spacing=1, font_file='font'):
        if len(text) <= 0:
            print('text.__init__: No text error')
            exit()
        self.text = text
        self.spacing = spacing
        self.font = Font(font_file)
        self.width = self.gen_width()
        self.height = self.gen_height()
        self.canvas = Image(
            width=self.width+len(self.text)*self.spacing-self.spacing,
            height=self.height
            )
        self.print()

    def gen_width(self):
        current_width = []
        width = []
        for i in self.text:
            for j in self.font.char(i):
                current_width.append(len(j))
            width.append(max(current_width))
            current_width = []
        return sum(width)

    def gen_height(self):
        height = [max([len(self.font.char(i)) for i in self.text])]
        return max(height)

    def print(self):
        cursor = 0
        for letter in self.text:
            self.canvas.paste(
                self.font.char(letter), x=cursor, y=0, mode='fill'
                )
            cursor += len(self.font.char(letter)[0]) + self.spacing
        return self.canvas

    def get_text(self):
        return self.canvas

if __name__ == '__main__':
    from streamtools import Stream
    streamer = Stream(matrix=True)
    im = Image()
    
    while True:
        entry = input('Text: ')
        text = Text(entry.lower())
        im.paste(text.get_text(),x=0,y=5)
        streamer.set_data_from_matrix(im.get_pixmap())
        streamer.send_to_serial()
        print(streamer)