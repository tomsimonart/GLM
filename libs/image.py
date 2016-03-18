#!/usr/bin/env python3

from libs.streamtools import Stream

class Image:
    def __init__(self, width=None, height=None, pixmap=None):
        self.width = width
        self.height = height
        self.pixmap = pixmap # pixmap as matrix

        if width == None and height == None and pixmap == None:
            self.width = 0
            self.height = 0
            self.blank()

        elif self.pixmap != None:
            self.auto_size()

        elif self.width != None or self.height != None:
            self.blank()

        # Size check
        else:
            if not self.check_width():
                self.fill_width()
            if not self.check_height():
                self.fill_height()

    def auto_size(self):
        self.width = max([len(i) for i in self.pixmap])
        self.height = len(self.pixmap)
        self.fill_width()
        self.fill_height()

    def check_width(self):
        return all(len(i) == self.width for i in self.pixmap)

    def fill_width(self):
        self.pixmap = [
            i[:self.width] + [0] * (self.width - len(i)) for i in self.pixmap
            ]

    def check_height(self):
        return len(self.pixmap) == self.height

    def fill_height(self):
        if len(self.pixmap) < self.height:
            self.pixmap = \
            self.pixmap + [[0] * self.width] * (self.height - len(self.pixmap))
        else:
            self.pixmap = self.pixmap[0:self.height]

    def resize(self, width, height):
        # Height
        if height < self.height:
            self.pixmap = self.pixmap[0:height]
        elif height > self.height:
            while len(self.pixmap) < height:
                self.pixmap.append([0] * self.width)
        # Width
        if width < self.width:
            self.pixmap = [i[:width] for i in self.pixmap]
        elif width > self.width:
            self.pixmap = [i + [0] * (width - self.width) for i in self.pixmap]

        self.height = height
        self.width = width

    def __str__(self):
        return str(self.pixmap)

    def __repr__(self):
        data = ['Image(', self.width, ',', self.height, ',', self.pixmap, ')']
        return str(''.join(map(str, data)))

    def get_pixmap(self):
        return self.pixmap

    def blank(self):
        self.pixmap = [
            [0 for j in range(self.width)] for i in range(self.height)
            ]

    def paste(self, image, x=0, y=0, mode='fill'):
        """ Paste an image over another, can take an image or a matrix
        as pixmap. x=0, y=0 -> Start location of the paste
        mode={fill, replace, invert}
        """
        try:
            if mode == 'fill':
                for i in range(y, image.height + y):
                    for j in range(x, image.width + x):
                        if i < self.height and j < self.width:
                            self.pixmap[i][j] |= image.get_pixmap()[i-y][j-x]
            elif mode == 'replace':
                for i in range(y, image.height + y):
                    for j in range(x, image.width + x):
                        if i < self.height and j < self.width:
                            self.pixmap[i][j] = image.get_pixmap()[i-y][j-x]
            elif mode == 'invert':
                for i in range(y, image.height + y):
                    for j in range(x, image.width + x):
                        if i < self.height and j < self.width:
                            self.pixmap[i][j] ^= image.get_pixmap()[i-y][j-x]
        except IndexError as e:
            print('paste:',e, i,j, x,y)

if __name__ == '__main__':
    from streamtools import Stream
    sample = [[1,0,1,0,1,0],[0,1,0,1,0,1],[0,0,1,0,1,0,1]]
    streamer = Stream(matrix=False)
    test = Image(width=64,height=16)
    test.draw_line(7, 7, 63, 15)
    test.draw_dot(60, 3)
    test.paste(sample, mode='fill', x=1, y=1)
    streamer.set_data_from_matrix(test.get_pixmap())
    print(streamer)