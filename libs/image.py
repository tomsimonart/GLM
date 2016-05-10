#!/usr/bin/env python3

from libs.streamtools import Stream
from libs.rainbow import msg


class Image:
    """
    An Image has a width a height and a boolean pixmap (matrix).
    All parameters are optional.

    You can specify the width and the height without pixmap.
    If you give a pixmap only, the Image will be autosized even if the sizes
    are not equal.

    Keyword arguments:
    width -- Image width (default None)
    height -- Image height (default None)
    pixmap -- matrix of binary data (default None)
    """
    def __init__(self, width=None, height=None, pixmap=None):
        self.width = width
        self.height = height
        self.pixmap = pixmap  # pixmap as matrix

        if width is None and height is None and pixmap is None:
            self.width = 0
            self.height = 0
            self.blank()

        elif width is not None and height is not None and pixmap is not None:
            self.resize(width, height)

        elif self.pixmap is not None:
            self.auto_size()

        elif self.width is not None or self.height is not None:
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
            self.pixmap = (
                self.pixmap +
                [[0] * self.width] * (self.height - len(self.pixmap)))
        else:
            self.pixmap = self.pixmap[0:self.height]

    def resize(self, width, height):
        """Resize Image"""
        self.auto_size()
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
        """Get the Image data"""
        return self.pixmap

    def blank(self):
        """Clear the Image"""
        self.pixmap = [
            [0 for j in range(self.width)] for i in range(self.height)
            ]

    def fill(self):
        """Fill the Image"""
        self.pixmap = [
            [1 for j in range(self.width)] for i in range(self.height)
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
            msg("paste error", 2, "Image.paste()")
