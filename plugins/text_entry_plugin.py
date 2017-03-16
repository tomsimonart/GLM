#!/usr/bin/env python3
from libs.screen import Screen
from libs.image import Image
from libs.text import Text
from os import system

screen = Screen(matrix=True, show=True, fps=2555)
label_1 = Text()
label_2 = Text()
screen.add(label_1, y=1)
screen.add(label_2, y=9)

while True:
    try:
        label_1.edit(input('Text line 1: '))
        label_2.edit(input('Text line 2: '))
        screen.refresh()
    except KeyboardInterrupt:
        print('\nEND')
        exit()