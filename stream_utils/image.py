#!/usr/bin/env python3

class Image():
    def __init__(self, width=None, height=None, pixmap=None):
        self.width = width
        self.height = height
        self.pixmap = pixmap # pixmap as matrix

        if width == None and height == None and pixmap == None:
            self.width = 64
            self.height = 16

        if self.height == None or self.width == None:
            self.auto_size()

        elif self.pixmap == None:
            self.pixmap = [
                [0 for j in range(self.width)] for i in range(self.height)
                ]
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

if __name__ == '__main__':
    table = [[1,1,0,1],[0,1],[0,0,0,0,0,1]]
    lol = Image(width=None, height=None, pixmap=table)
    print(lol)
    troll = Image()