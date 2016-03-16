#!/usr/bin/env python3

from libs.text import Text
from libs.image import Image
from libs.screen import Screen
from libs.streamtools import Stream

class ExamplePlugin:
    def __init__(self):
        self.screen = Screen(matrix=False, show=True, fps=1)
        self.label = Text()
        self.drawing = Image(width=10, height=10)
        self.screen.add(self.drawing)
        self.screen.add(self.label)

    def stream(self):
        for i in range(10):
            self.drawing.draw_line(i, 0, 9, i)
            self.label.edit(str(i))
            self.screen.refresh()

if __name__ == '__main__':
    plugin = ExamplePlugin()
    plugin.stream()
