#!/usr/bin/env python3

from libs.text import Text
from libs.image import Image
from libs.streamtools import Screen, Stream

class ExamplePlugin:
    def __init__(self):
        self.label = Text('1')
        self.image = Image()
        self.streamer = Stream()
        #self.screen = Screen(self.image)

    def stream(self):
        for i in range(1):
            self.label = Text(str(i))
            #self.image.blank()
            self.image.draw_line(0,0,63,15)
            self.image.paste(self.label)
            #print(self.image.get_pixmap())
            self.streamer.set_data_from_matrix(self.image.get_pixmap())
            self.streamer.send_to_serial()


if __name__ == '__main__':
    plugin = ExamplePlugin()
    plugin.stream()
