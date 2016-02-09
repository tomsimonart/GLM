#Made in one caffeine fueled weekend by Minorias

import time,os
class HImage:
    matrix_height = 16
    matrix_width = 64
    def __init__(self, width = matrix_width, height = matrix_height, pixelmatrix = []):   
        if len(pixelmatrix) == 0: #empty matrix
            self.width = width
            self.height = height
            self.pixels = [[0 for i in range(self.width)] for j in range(self.height)]
        
        else:                   #matrix with data in it
            if all(len(pixelmatrix[i]) == pixelmatrix[0] for i in range(len(pixelmatrix))):
                self.pixels = pixeldata
            else:
                standard_width = max([len(pixelmatrix[i]) for i in range(len(pixelmatrix))])
                for line in pixelmatrix:
                    while len(line) < standard_width:
                        line.append(0)
                self.pixels = pixelmatrix
            self.width = len(pixelmatrix[0])
            self.height = len(pixelmatrix)
                
    
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
  #          print("Clip you selected is too long, resetting back to max matrix width.")
            width = self.width - x_coord#- (x_coord + width)

        if y_coord + height > self.height:
    #        print("Clip you selected is too high, resetting back to max matrix height.")
            height = self.height - y_coord# - (y_coord + height)

        pix = [[self[(x_coord+x, y_coord+y)] for x in range(width)] for y in range(height)]
        return HImage(pixelmatrix=pix)

    
    def paste(self, another_image, x_coord=0, y_coord=0):
        required_width = x_coord + another_image.width 
        required_height = y_coord + another_image.height
        if required_width > self.width:
            for line in self.pixels:
                while len(line) < required_width:
                        line.append(0)
        if required_height > self.height:
            if required_height > self.matrix_height:
                print("That thing you're trying to paste is making the matrix taller than 16, watch out!")
            while len(self.pixels) < required_height:
                self.pixels.append([0 for i in range(max(self.matrix_width,required_width,self.width))])
        
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
                print("That thing you're trying to paste is making the matrix taller than 16, watch out!")
            while len(self.pixels) < required_height:
                self.pixels.append([0 for i in range(max(self.matrix_width,required_width,self.width))])
       
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
        required_height = y_coord + another_image.height + self.height +separation
        
        if required_width > self.width:
            for line in self.pixels:
                while len(line) < required_width:
                        line.append(0)
        
        if required_height > self.height:
            if required_height > self.matrix_height:
                print("That thing you're trying to insert above that other thing is making the matrix taller than 16, watch out!")
            while len(self.pixels) < required_height:
                self.pixels.insert(0,[0 for i in range(max(self.matrix_width,required_width,self.width))])

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

T, _ = 1, 0
star = HImage(pixelmatrix=[
    [ T, _, _, T, _, _, T],
    [ _, T, _, T, _, T, _],
    [ _, _, T, T, T, _, _],
    [ T, T, T, T, T, T, T],
    [ _, _, T, T, T, ],
    [ _, T, _, T, _, T, ],
    [ T, _, _, T, _, _, T],
])

star2 = HImage(pixelmatrix=[
    [ T, _, _, T, _, _, T],
    [ _, T, _, T, _, T, _],
    [ _, _, T, T, T, _, _],
    [ T, T, T, T, T, T, T],
    [ _, _, T, T, T, ],
    [ _, T, _, T, _, T, ],
    [ T, _, _, T, _, _, T],
    
])


def text(text, font={}):
    letters = [font.get(letter,font[" "]) for letter in text]
    total_width = sum(letter.width for letter in letters)
    total_height = max(letter.height for letter in letters)
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
    return {p[0]: HImage(pixelmatrix=[[int(x) for x in l] for l in p[1:].strip().split()]) for p in parts}

font = load_font("font file.txt")
font[' '] = HImage(width=3, height=5)

img_1 = text("HELLO TOM HOW ARE YOU DOING",font)
img_2 = text("YOLOBLAZEITEVERYDAY",font)
#print(img_1.width,img_2.width)
#img_1.paste(img_2, x_coord=(img_1.width - img_2.width)//2, y_coord=img_1.height+1)
img_3 = text("BLA",font)
img_1.insert_above(img_2)
img_1.insert_before(img_3)
img_1.fun()
















while 1:
    for i in range(img_1.width-64):
        img_1.clip(x_coord = i, y_coord = 0, width = 64,height = 15).normalise().display()
        
        time.sleep(0.1)
        os.system("clear")
    for i in range(img_1.width-64,-1,-1):
        img_1.clip(x_coord = i, y_coord = 0, width = 64,height = 15).normalise().display()
        time.sleep(0.1)
        os.system("clear")


    for i in range(img_1.height+1):
        img_1.clip(x_coord = 0, y_coord = i, width = 64,height = 15).normalise().display()
        time.sleep(0.1)
        os.system("clear")
    for i in range(img_1.height+1,-1,-1):
        img_1.clip(x_coord = 0, y_coord = i, width = 64,height = 15).normalise().display()
        time.sleep(0.1)
        os.system("clear")



"""
star.paste(star2,star.width+1)
star.paste(star2,star.width+1)
star.paste(star2,star.width+1)
star.paste(star2,star.width+1)
star.paste(star2,star.width+1)
# star.paste(star,0,star.height+1)
star.paste(star,0,star.height+1)
star.paste(star,star.width+1,0)
# star.paste(star,0,star.height+1)




# while 1:
#     for i in range(star.width+1):
#         star.clip(x_coord = i, y_coord = 0, width = 64,height = 15).normalise().display()
#         time.sleep(0.09)
#         os.system("clear")
#     for i in range(star.width+1,-1,-1):
#         star.clip(x_coord = i, y_coord = 0, width = 64,height = 15).normalise().display()
#         time.sleep(0.09)
#         os.system("clear")


#     for i in range(star.height+1):
#         star.clip(x_coord = 0, y_coord = i, width = 64,height = 15).normalise().display()
#         time.sleep(0.09)
#         os.system("clear")
#     for i in range(star.height+1,-1,-1):
#         star.clip(x_coord = 0, y_coord = i, width = 64,height = 15).normalise().display()
#         time.sleep(0.09)
#         os.system("clear")


# while True:
#     for i in range(star.height+1):
#         star.clip(i,i,64,16).normalise().display()
#         time.sleep(0.1)
#         os.system("clear")

#     for i in range(star.height,-1,-1):
#         star.clip(i,i,64,16).normalise().display()
#         time.sleep(0.1)
#         os.system("clear")

"""