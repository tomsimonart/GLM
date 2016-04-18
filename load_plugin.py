#!/usr/bin/env python3

from libs.screen import Screen
from libs.text import Text
from libs.image import Image

class LoadPlugin:
    def __init__(self):
        self.screen = Screen(matrix=True, show=True, fps=28)
        self.label = Text("download")
        self.loading = Text()
        self.load = [' l','/','-','\\']
        self.screen.add(self.label, refresh=False, x=0, y=0)
        self.screen.add(self.loading, refresh=True, x=29,y=8)

    def stream(self):
        while True:
            for i in self.load:
                self.loading.edit(i)
                self.screen.refresh()
        #self.loading.edit('b')
        #self.screen.refresh()


if __name__ == '__main__':
    plugin = LoadPlugin()
    plugin.stream()