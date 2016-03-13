#!/usr/bin/env python3

#Made in one caffeine fueled weekend by Minorias

import time
import os
from libs.streamtools import Stream

class HImage(Stream):
    matrix_height = 16
    matrix_width = 64
    def __init__(
        self,
        width = matrix_width,
        height = matrix_height,
        pixelmatrix = []):
        if len(pixelmatrix) == 0: #empty matrix
            self.width = width
            self.height = height
            self.pixels = [
                [0 for i in range(self.width)] for j in range(self.height)
                ]
        
        # Matrix with data in it
        else:
            if all(len(pixelmatrix[i]) == len(pixelmatrix[0]) for i in range(len(pixelmatrix))):
                self.pixels = pixeldata
            else:
                standard_width = max(
                    [len(pixelmatrix[i]) for i in range(len(pixelmatrix))]
                    )
                for line in pixelmatrix:
                    while len(line) < standard_width:
                        line.append(0)
                self.pixels = pixelmatrix
            self.width = len(pixelmatrix[0])
            self.height = len(pixelmatrix)

        Stream.__init__(self, self.height, self.width)
        print(Stream, self.height)

    def __getitem__(self,position):
        x,y = position
        return self.pixels[y][x]                

    
    def __setitem__(self,position,value):
        x,y = position
        if value in [1,0]:
            self.pixels[y][x] = value

    
    def led_output(self):
        return self.pixels

    
    def display(self):
        for y in range(self.height):
            for x in range(self.width):
                if self[(x, y)] == 1:
                    print("\033[41m \033[0m", end='')
                else:
                    print("\033[44m \033[0m", end='')
            print()

    
    def normalise(self):
        if self.width != self.matrix_width:
            for i in range(len(self.pixels)):
                self.pixels[i] = self.pixels[i][:self.matrix_width]
                while len(self.pixels[i]) < self.matrix_width:
                    self.pixels[i].append(0)

        
        if self.height != self.matrix_height:
            self.pixels = self.pixels[:self.matrix_height]
            while len(self.pixels) < self.matrix_height:
                self.pixels.append([0 for i in range(self.matrix_width)])

        self.width = len(self.pixels[0])
        self.height = len(self.pixels)
        
        return self

    
    def clip(self,x_coord = 0, y_coord = 0, width = 1, height = 1):
        if x_coord + width > self.width:
            # print("Clip you selected is too long,
            # resetting back to max matrix width.")
            width = self.width - x_coord#- (x_coord + width)

        if y_coord + height > self.height:
            # print("Clip you selected is too high,
            # resetting back to max matrix height.")
            height = self.height - y_coord# - (y_coord + height)

        pix = [
            [self[(x_coord+x, y_coord+y)
            ] for x in range(width)] for y in range(height)]
        return HImage(pixelmatrix=pix)

    
    def paste(self, another_image, x_coord=0, y_coord=0):
        required_width = x_coord + another_image.width 
        required_height = y_coord + another_image.height

        for elem in another_image.pixels:
            print(len(elem), elem, another_image.width)

        print(x_coord, another_image.width, required_width)
        print(y_coord, another_image.height, required_height)
        if required_width > self.width:
            print("hello")
            for line in self.pixels:
                while len(line) < required_width:
                    line.append(0)
        if required_height > self.height:
            if required_height > self.matrix_height:
                print("That thing you're trying to paste is making the matrix "
                    "taller than 16, watch out!")
            while len(self.pixels) < required_height:
                self.pixels.append([0 for i in range(max(
                    required_width,self.width
                    ))])
        
        print('xhcek', another_image.width, another_image.height)
        for x in range(another_image.width):
            for y in range(another_image.height):
                self[(x+x_coord, y+y_coord)] = another_image[(x, y)]
        self.width = len(self.pixels[0])
        self.height = len(self.pixels)
    
    
    def insert_before(self,another_image=None,x_coord = 0, y_coord = 0):
        required_height = y_coord + another_image.height
        required_width = self.width + another_image.width + x_coord
        
        if required_height > self.height:
            if required_height > self.matrix_height:
                print("That thing you're trying to paste is making the matrix "
                    "taller than 16, watch out!")
            while len(self.pixels) < required_height:
                self.pixels.append([0 for i in range(max(
                    self.matrix_width,required_width,self.width
                    ))])
       
        for row in self.pixels:
            while len(row) < required_width:
                row.insert(0,0)

        for x in range(another_image.width):
            for y in range(another_image.height):
                self[(x+x_coord, y+y_coord)] = another_image[(x, y)]
        
        self.width = len(self.pixels[0])
        self.height = len(self.pixels)


    def insert_above(self, another_image, x_coord=0, y_coord=0,separation=1):
        required_width = x_coord + another_image.width 
        required_height = (
            y_coord +
            another_image.height +
            self.height +
            separation)
        
        if required_width > self.width:
            for line in self.pixels:
                while len(line) < required_width:
                        line.append(0)
        
        if required_height > self.height:
            if required_height > self.matrix_height:
                print("That thing you're trying to insert above that other "
                    "thing is making the matrix taller than 16, watch out!")
            while len(self.pixels) < required_height:
                self.pixels.insert(0,[0 for i in range(max(
                    required_width,self.width
                    ))])

        for x in range(another_image.width):
            for y in range(another_image.height):
                self[(x+x_coord, y+y_coord)] = another_image[(x, y)]
        
        self.width = len(self.pixels[0])
        self.height = len(self.pixels)    

    def fun(self):
        #Because why the fuck not?
        for row in self.pixels:
            row.reverse()
        self.pixels.reverse()

def text(text, font={}):
    letters = [font.get(letter,font[" "]) for letter in text]
    total_width = sum(letter.width for letter in letters)
    total_height = max(letter.height for letter in letters)
    print('wh',total_width, total_height)
    text_img= HImage(width=total_width, height=total_height)
    x = 0
    y = 0
    for letter in letters:
        text_img.paste(letter, x_coord=x, y_coord=y)
        x += letter.width
    return text_img


def load_font(fontfile):
    contents = open(fontfile).read().strip()
    parts = filter(len, contents.split('--'))
    res = {}
    for p in parts:
        res[p[0]] = HImage(pixelmatrix=[[int(x) for x in l] for l in p[1:].strip().split()])
        print(res[p[0]].width)
    return res

font = load_font("fonts/charmap")
font[' '] = HImage(width=3, height=5)

img_1 = text("MINORIAS",font)
img_2 = text("INFECTED",font)
img_3 = text("BLA",font)

img_1.insert_above(img_2)
img_1.insert_before(img_3)
# img_1.fun()

while 1:
    for i in range(img_1.width-64):
        img_1.clip(x_coord = i, y_coord = 0, width = 64,height = 15).\
            normalise().display()
        time.sleep(0.1)
        os.system("clear")

    for i in range(img_1.width-64,-1,-1):
        img_1.clip(x_coord = i, y_coord = 0, width = 64,height = 15).\
            normalise().display()
        time.sleep(0.1)
        os.system("clear")

    for i in range(img_1.height+1):
        img_1.clip(x_coord = 0, y_coord = i, width = 64,height = 15).\
            normalise().display()
        time.sleep(0.1)
        os.system("clear")

    for i in range(img_1.height+1,-1,-1):
        img_1.clip(x_coord = 0, y_coord = i, width = 64,height = 15).\
            normalise().display()
        time.sleep(0.1)
        os.system("clear")