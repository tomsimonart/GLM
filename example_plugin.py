#!/usr/bin/env python3

from libs.text import Text
from libs.image import Image
from libs.screen import Screen
from libs.streamtools import Stream

class ExamplePlugin:
    def __init__(self):
        self.image = Image()
        self.screen = Screen(self.image, matrix=False, show=True)
        self.label = Text('12345')
        self.drawing = Image(width=10, height=10)
        self.screen.add(self.drawing)
        self.screen.add(self.label, refresh=False)

        self.streamer = Stream(matrix=False)
        self.label.resize(64, 16)
        self.streamer.set_data(self.label)
        print(self.streamer)

    def stream(self):
        for i in range(10):
            self.drawing.draw_line(i, 0, 9, i)
            self.label = Text(str(i))
            self.screen.refresh()

if __name__ == '__main__':
    plugin = ExamplePlugin()
    #plugin.stream()
