#!/usr/bin/env python3

from libs.text import Text
from libs.image import Image
from libs.streamtools import Screen, Stream

class ExamplePlugin:
    def __init__(self):
        self.label = Text('1')
        self.image = Image()
        self.streamer = Stream(matrix=False)
        #self.screen = Screen(self.image)

    def stream(self):
        for i in range(10):
            self.label = Text(str(i))
            self.image.blank()
            self.image.paste(self.label)
            #self.image.paste(Image(pixmap=[[1,1,1,1],[1,0,0,1],[1,1,1,1]]),x=10,y=5,mode='fill')
            self.streamer.set_data_from_matrix(self.image.get_pixmap())
            self.streamer.send_to_serial()
            print(self.streamer)


if __name__ == '__main__':
    plugin = ExamplePlugin()
    plugin.stream()
