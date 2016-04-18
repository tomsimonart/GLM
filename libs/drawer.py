#!/usr/bin/env python3


class Drawer:
    def __init__(self, image):
        self.image = image

    def dot(self, x, y):
        if x < self.image.width and y < self.image.height:
            self.image.pixmap[y][x] = 1
        else:
            print('dot: outside image', x, y)

    def erase(self, x, y):
        if x < self.image.width and y < self.image.height:
            self.image.pixmap[y][x] = 0
        else:
            print('erase: outside image', x, y)

    def line(self, x1, y1, x2, y2):
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
            self.dot(coord[0], coord[1])