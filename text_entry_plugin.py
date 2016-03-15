#!/usr/bin/env python3
from libs.streamtools import Stream
from libs.image import Image
from libs.text import Text
from os import system

streamer = Stream(matrix=True)
im = Image()

while True:
    print(streamer)
    entry = input('Text line 1: ')
    entry2 = input('Text line 2: ')
    if entry == '':
        entry = ' '
    if entry2 == '':
        entry2 = ' '

    system('clear')
    im.blank()
    text = Text(entry.lower())
    text2 = Text(entry2.lower())
    im.paste(text.get_text(),x=0,y=1)
    im.paste(text2.get_text(),x=0, y=9)
    streamer.set_data_from_matrix(im.get_pixmap())
    streamer.send_to_serial()