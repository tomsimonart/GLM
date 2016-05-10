#!/usr/bin/env python3

from .image import Image
from .streamtools import MAT_WIDTH, MAT_HEIGHT
from time import sleep
from .rainbow import msg

R = 'right'
L = 'left'
U = 'up'
D = 'down'
RU = 'right_up'
LU = 'left_up'
RD = 'right_down'
LD = 'left_down'
F = 'fluid'
S = 'stop'

class Slide:
    """
    Slide is used to scroll one Image
    """
    def __init__(
            self,
            image,
            direction=R,
            spacing=1,
            width=MAT_WIDTH,
            height=MAT_HEIGHT,
            ):

        self.image = image
        self.width = width
        self.height = height
        self.view = Image(width=self.width, height=self.height)
        self.spacing = spacing
        self.direction = direction
        self.x_pos = 0
        self.y_pos = 0

    def refresh(self, mode='left', spacing=5, step=1):
        spacing_x = self.image.width - self.width + spacing
        spacing_y = self.image.height - self.height + spacing
        x = self.x_pos % (self.width + spacing_x)
        y = self.y_pos % (self.height + spacing_y)
        x2 = x - self.width - spacing_x
        y2 = y - self.height - spacing_y

        self.view.paste(self.image, x, y)
        self.view.paste(self.image, x2, y)
        self.view.paste(self.image, x, y2)
        self.view.paste(self.image, x2, y2)

        if mode == 'up':
            self.shift_up(step)
        if mode == 'down':
            self.shift_down(step)
        if mode == 'left':
            self.shift_left(step)
        if mode == 'right':
            self.shift_right(step)

    def shift_right(self, step=1):
        self.x_pos += step

    def shift_left(self, step=1):
        self.x_pos -= step

    def shift_up(self, step=1):
        self.y_pos -= step

    def shift_down(self, step=1):
        self.y_pos += step
