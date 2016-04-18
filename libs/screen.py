from libs.streamtools import Stream
from libs.image import Image
from os import system
from time import sleep

class Screen:
    def __init__(self, x=0, y=0, matrix=True, show=False, fps=0):
        if fps > 0:
            self.fps = 1 / fps
        else:
            self.fps = 0
        self.image = Image(width=64, height=16)
        self.streamer = Stream(matrix=matrix)
        self.show = show
        self.childs = []

    def add(self, image, x=0, y=0, refresh=True, mode='fill'):
        self.childs.append((image, x, y, refresh, mode))

    def refresh(self):
        self.image.blank()
        for screen in self.childs:
            self.image.paste(screen[0],
                x=screen[1],
                y=screen[2],
                mode=screen[4])

            # Refresh
            if screen[3]:
                screen[0].blank()

        self.streamer.set_data(self.image)
        self.streamer.send_to_serial()
        if self.show:
            system('clear')
            print(self.streamer)
        sleep(self.fps)
