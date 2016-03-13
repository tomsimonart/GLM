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

    def set_pixmap(self, pixmap):
        self.pixmap = pixmap

    def blank(self):
        self.pixmap = [
            [0 for j in range(self.width)] for i in range(self.height)
            ]

    def paste(self, pixmap, x=0, y=0, mode='fill'):
        """ Paste an image over another, can take an image or a matrix
        as pixmap. x=0, y=0 -> Start location of the paste
        mode={fill, replace, invert}
        """
        if not hasattr(pixmap, 'pixmap'):
            pixmap = Image(pixmap=pixmap)
        pixmap.resize(self.width, self.height)

        try:
            if mode == 'fill':
                for i in range(y, self.height):
                    for j in range(x, self.width):
                        self.pixmap[i][j] |= pixmap.get_pixmap()[i][j]
            elif mode == 'replace':
                for i in range(y, self.height):
                    for j in range(x, self.width):
                        self.pixmap[i][j] = pixmap.get_pixmap()[i][j]
            elif mode == 'invert':
                for i in range(y, self.height):
                    for j in range(x, self.width):
                        self.pixmap[i][j] ^= pixmap.get_pixmap()[i][j]
        except IndexError:
            print('Paste failed: IndexError')

    def draw_dot(self, x, y):
        if x < self.width and y < self.height:
            self.pixmap[y][x] = 1
        else:
            print('draw_dot: outside image', x, y)

    def draw_line(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        is_steep = abs(dy) > abs(dx)
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        swapped = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2  = y2, y1
            swapped = True
        dx = x2 - x1
        dy = y2 - y1
        error = int(dx / 2.0)
        ystep = 1 if y1 < y2 else -1
        y = y1
        points = []
        for x in range(x1, x2 + 1):
            coord = (y, x) if is_steep else (x,y)
            points.append(coord)
            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx
        if swapped:
            points.reverse()
        for coord in points:
            self.draw_dot(coord[0], coord[1])

if __name__ == '__main__':
    from streamtools import Stream
    sample = Image(pixmap=[[1,0,1,0,1,0],[0,1,0,1,0,1],[0,0,1,0,1,0,1]])
    streamer = Stream(matrix=False)
    test = Image(width=64,height=16)
    test.draw_line(7, 7, 63, 15)
    test.draw_dot(60, 3)
    test.paste(sample, mode='fill')
    streamer.set_data_from_matrix(test.get_pixmap())
    print(streamer)