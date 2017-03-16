#!/usr/bin/env python3

from libs.text import Text
from libs.image import Image
from libs.screen import Screen
from libs.drawer import Drawer
from libs.streamtools import Stream
from libs.rainbow import msg

class ExamplePlugin:
    def __init__(self):
        self.screen = Screen(matrix=False, show=True, fps=23)
        self.label = Text()
        self.drawing = Image(64, 16)
        self.drawer = Drawer(self.drawing)
        self.screen.add(self.drawing)
        self.screen.add(self.label)

    def stream(self):
        for i in range(1, 101):
            self.drawer.line(i, 0, 9, i)
            self.label.edit(str(i))
            self.screen.refresh()
            msg("Progression", 0, None, i)


if __name__ == '__main__':
    plugin = ExamplePlugin()
    plugin.stream()
