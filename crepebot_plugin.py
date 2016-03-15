#!/usr/bin/env python3
# Crepe bot plugin by infected

from libs.streamtools import Stream
from libs.text import Text
from libs.image import Image
from libs import pbmtools

class CrepeBot:
    def __init__(self, percentage=0):
        self.percentage = percentage
        self.percentage_text = Text(str(percentage))
        self.pbm = Image()
        self.bar = Image()
        self.bar_x = 40
        self.bar_y = 7
        self.image = Image()
        self.stream = Stream(matrix=True)
        self.splash = Text('crepe bot')

    def refresh(self, percentage):
        self.percentage = percentage
        self.percentage_text = Text(str(percentage)+'%')
        self.image.blank()
        self.image.paste(self.splash.get_text(), x=25, y=0)
        self.refresh_bar(percentage)
        self.image.paste(self.bar.get_pixmap(), x=self.bar_x, y=self.bar_y)
        self.image.paste(self.percentage_text.get_text(), x=40, y=10)

        self.stream.set_data_from_matrix(self.image.get_pixmap())
        self.stream.send_to_serial()
        print(self.stream)

    def refresh_bar(self, percentage):
        if percentage % 5 == 0:
            self.bar.draw_dot(x=0 + percentage // 5, y=0)
            self.bar.draw_dot(x=0 + percentage // 5, y=1)

if __name__ == '__main__':
    from time import sleep
    plugin = CrepeBot()
    #sleep(1)
    for i in range(101):
        plugin.refresh(i)
        #sleep(0.1)
