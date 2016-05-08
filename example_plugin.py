#!/usr/bin/env python3

from libs.text import Text
from libs.image import Image
from libs.screen import Screen
from libs.drawer import Drawer
from libs.streamtools import Stream

class ExamplePlugin:
    def __init__(self):
        self.screen = Screen(matrix=True, show=True, fps=1)
        self.label = Text()
        self.drawing = Image(width=45, height=15)
        self.drawer = Drawer(self.drawing)
        self.screen.add(self.drawing)
        self.screen.add(self.label)

    def stream(self):
        for i in range(10):
            self.drawer.line(i, 0, 9, i)
            self.drawer.dot(15, 12)
            self.label.edit(str(i))
            self.screen.refresh()

if __name__ == '__main__':
    plugin = ExamplePlugin()
    plugin.stream()
