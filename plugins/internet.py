from libs.screen import Screen
from libs.image import Image
from libs.text import Text
from libs.drawer import Drawer
from libs.rainbow import color, msg
from libs.slide import Slide, L
from time import sleep
import traceback as tb
from sys import exc_info

class Plugin():
    """docstring for Plugin"""
    def __init__(self, matrix=True, show=False):
        super(Plugin, self).__init__()
        self.version = "0.0.2"
        self.author = "Infected"
        self.name = "Internet Plugin"

        self.label = Text("urlab is love,")
        self.label_2 = Text("urlab is life.")
        self.label.resize(int(self.label.width * 1.5), self.label.height)
        self.label_2.resize(int(self.label.width * 1.5), self.label_2.height)
        self.slider = Slide(self.label, L, 0, self.label.width, self.label.height)
        self.slider_2 = Slide(self.label_2, L, 0, self.label.width, self.label.height)

        self.screen = Screen(matrix=matrix, show=show)
        self.screen.add(self.slider, refresh=True)
        self.screen.add(self.slider_2, refresh=True, y=8)

    def start(self):
        n = 0
        while True:
            self.slider.refresh(mode='left', spacing=0, step=1)
            self.slider_2.refresh(mode='left', spacing=0, step=1)
            self.screen.refresh()
            msg('refersh %i' % n)
            n+=1
            print(exc_info())
