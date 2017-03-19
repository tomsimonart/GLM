#!/usr/bin/env python3

from libs.screen import Screen
from libs.text import Text
from libs.image import Image
from libs.rainbow import msg
from time import sleep


class LoadPlugin:
    def __init__(self, matrix=True, show=False, fps=35):
        super(LoadPlugin, self).__init__()
        self.version = "0.0.1"
        self.screen = Screen(matrix=matrix, show=show, fps=fps)

        self.label = Text("download")
        self.loading = Text(font="fontbignum")
        self.percent = Text("0%")
        self.load = [' l', '/', '-', '\\']

        self.screen.add(self.label, refresh=False, x=0, y=0)
        self.screen.add(self.loading, refresh=True, x=29, y=8)
        self.screen.add(self.percent, refresh=False, x=0, y=6)

    def start(self):
        msg("Starting download...", 2, "Download", "0%")
        for p in range(0, 101):
            self.percent.blank()
            self.percent.edit(p, font="fontbignum")
            for i in self.load:
                self.loading.edit(i)
                self.screen.refresh()
            msg("Downloading...", 1, "Download", "{0}%".format(p))
        msg("Done", 0, "Download", "100%")
