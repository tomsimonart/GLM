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
            self.is_pixmap(self.pixmap)
            self.auto_size()

        elif self.width is not None or self.height is not None:
            self.blank()

        # Size check
        else:
            if not self.check_width(self.pixmap):
                self.fill_width()
            if not self.check_height(self.pixmap):
                self.fill_height()

    def is_pixmap(self, pixmap):
        """
        Check if the given pixmap has a pixmap format.
        Tell you what is wrong and kill the program if it is not the case.
        """
        if type(pixmap) is list:
            if type(pixmap[0]) is list:
                for i in pixmap:
                    for j in i:
                        if j != 0 and j != 1:
                            msg("pixmap wrong data !(1|0)", 3, "Image", j, i)
                            exit()
            else:
                msg("pixmap is not a matrix", 3, "Image", type(pixmap[0]))
                exit()
        else:
            msg("pixmap is not a matrix", 3, "Image", type(pixmap))
            exit()

    def auto_size(self):
        """Auto fill width and height"""
        self.width = max([len(i) for i in self.pixmap])
        self.height = len(self.pixmap)
        self.fill_width()
        self.fill_height()

    def check_width(self, pixmap):
        """
        Check if the width of the image is the same as the width of the pixmap
        """
        return all(len(i) == self.width for i in pixmap)

    def get_pixmap_width(self, pixmap):
        """Get the width of a pixmap"""
        return max(len(i) for i in pixmap)

    def fill_width(self):
        """Fills the remaining width of the pixmap with 0"""
        self.pixmap = [
            i[:self.width] + [0] * (self.width - len(i)) for i in self.pixmap
            ]

    def check_height(self, pixmap):
        """
        Check if the height of the image is the same as the height of the
        pixmap
        """
        return len(pixmap) == self.height

    def get_pixmap_height(self, pixmap):
        """Get the height of a pixmap"""
        return len(pixmap)

    def fill_height(self):
        """Fills the remaining height of the pixmap with 0"""
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

    def set_pixmap(self, pixmap):
        """Set a new pixmap and check for width and height"""
        self.is_pixmap(pixmap)
        pixmap_height = self.get_pixmap_height(pixmap)
        pixmap_width = self.get_pixmap_width(pixmap)
        if pixmap_height > self.height:
            msg("pixmap too high", 2, "Image.set_pixmap()", pixmap_height)
        if pixmap_width > self.width:
            msg("pixmap too large", 2, "Image.set_pixmap()", pixmap_width)
        self.pixmap = pixmap
        self.resize(self.width, self.height)

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
        """
        Paste an Image over another, can take an image or a pixmap.

        Keyword arguments:
        image -- Image
        x -- x location (default 0)
        y -- y location (default 0)
        mode -- paste mode (default 'fill')
            ['fill', 'replace', 'invert', 'modulo']
        """
        if mode == 'fill':
            for i in range(y, image.height + y):
                for j in range(x, image.width + x):
                    if i < self.height and j < self.width:
                        if i >= 0 and j >= 0:
                            self.pixmap[i][j] |= image.get_pixmap()[i-y][j-x]

        elif mode == 'replace':
            for i in range(y, image.height + y):
                for j in range(x, image.width + x):
                    if i < self.height and j < self.width:
                        if i >= 0 and j >= 0:
                            self.pixmap[i][j] = image.get_pixmap()[i-y][j-x]

        elif mode == 'invert':
            for i in range(y, image.height + y):
                for j in range(x, image.width + x):
                    if i < self.height and j < self.width:
                        if i >= 0 and j >= 0:
                            self.pixmap[i][j] ^= image.get_pixmap()[i-y][j-x]

        elif mode == 'modulo':
            for i in range(y, image.height + y):
                for j in range(x, image.width + x):
                    self.pixmap[i % self.height][j % self.width] |= (
                        image.get_pixmap()[i-y][j-x])

        else:
            msg("no such paste mode", 2, "Image.paste()", mode)
