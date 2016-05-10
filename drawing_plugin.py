#!/usr/bin/env python3

import tkinter
import threading
import time
from libs.image import Image
from libs.drawer import Drawer
from libs.screen import Screen

# INSTRUCTIONS
#   CLICKING 2 DOTS AND THEN A LINE BETWEEN THEM APPEARS
#   CLICKING 2 DOTS AND A SQUARE BETWEEN THEM APPEARS
#   WRITING TEXT
#   SAVING / LOADING AN IMAGE


class Updater():
    def __init__(self, interface):
        self.interface = interface
        self.screen = Screen(matrix=False, show=False, fps=50)
        self.screen.add(self.interface.image, refresh=False)
        self.livestream = True

    def one_refresh(self):
        self.screen.refresh()

    def toggle_livestream(self):
        while self.livestream:
            self.screen.refresh()


class MatrixDrawer:
    def __init__(self, x=64, y=16):
        self.image = Image(width=x, height=y)
        self.drawer = Drawer(self.image)

        self.x = x
        self.y = y
        self.live = False
        self.drawmode = True

        self.create_window()
        self.create_canvas()
        self.create_buttons()

    def create_window(self):
        self.root = tkinter.Tk()
        self.root.configure(bg="light blue")

        self.root.bind("<Button-1>", self.mouse_interact_left)
        self.root.bind("<B1-Motion>", self.mouse_interact_left)
        self.root.bind("<Button-3>", self.mouse_interact_right)
        self.root.bind("<B3-Motion>", self.mouse_interact_right)

    def create_canvas(self):
        self.canvasframe = tkinter.Frame(self.root)
        self.canvasframe.pack(side="right")
        pixel_size = 20
        self.canvas = tkinter.Canvas(self.canvasframe, bg="black",
                                     height=self.y*pixel_size,
                                     width=self.x*pixel_size)

        self.canvas.grid(row=0, column=0)

        for y in range(self.y):
            for x in range(self.x):
                self.canvas.create_oval(x*pixel_size, y*pixel_size,
                                        x*pixel_size + pixel_size,
                                        y*pixel_size + pixel_size,
                                        fill="grey")

    def create_buttons(self):
        self.buttonframe = tkinter.Frame(self.root, bg="light blue")
        self.buttonframe.pack(side="left")
        self.terminalbutton = tkinter.Button(self.buttonframe,
                                             text="Send To Matrix",
                                             bg="Yellow",
                                             command=self.update_pixmap
                                             )
        self.clearbutton = tkinter.Button(self.buttonframe,
                                          text="Clear All",
                                          bg="Yellow",
                                          command=self.clearall
                                          )

        self.fillbutton = tkinter.Button(self.buttonframe,
                                         text="Fill All",
                                         bg="Yellow",
                                         command=self.fillall
                                         )
        self.livebutton = tkinter.Button(self.buttonframe,
                                         text="Status: Manual",
                                         bg="Yellow",
                                         command=self.togglelive
                                         )
        self.drawbutton = tkinter.Button(self.buttonframe,
                                         text="Draw Mode",
                                         bg="Yellow",
                                         command=self.toggleerase
                                         )
        self.erasebutton = tkinter.Button(self.buttonframe,
                                          text="Erase Mode",
                                          bg="Yellow",
                                          command=self.toggledraw
                                          )

        self.terminalbutton.grid(row=0, column=0, columnspan=2)
        self.clearbutton.grid(row=1, column=0, columnspan=2)
        self.fillbutton.grid(row=2, column=0, columnspan=2)
        self.livebutton.grid(row=3, column=0, columnspan=2)
        self.drawbutton.grid(row=4, column=0)
        self.erasebutton.grid(row=4, column=1)

    def toggledraw(self):
        self.drawmode = True
        # self.drawbutton.configure(relief=)

    def toggleerase(self):
        self.drawmode = False

    def togglelive(self):
        if self.live:   # we were already live, going manual now
            self.livebutton.configure(text="Status: Manual")
            self.live = False
        else:           # we were manual, now going live
            self.livebutton.configure(text="Status: Live  ")
            self.live = True
            self.live_update()

    def live_update(self):
        if self.live:
            self.screen.refresh()
            self.root.after(150, self.live_update)

    def clearall(self):
        """
        Clears all pixels, resetting them back to grey
        """
        for i in range(self.x * self.y):
            self.canvas.itemconfig(i+1, fill="grey")

        self.image.blank()

    def fillall(self):
        """
        Fills all pixels, setting them to red
        """
        for i in range(self.x * self.y):
            self.canvas.itemconfig(i+1, fill="red")

        self.image.fill()

    def mouse_interact_left(self, event):
        if event.widget.winfo_id() == self.canvas.winfo_id():
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)

            pixel = self.canvas.find_closest(x, y)

            self.canvas.itemconfig(pixel, fill="red")
            self.drawer.dot((pixel[0]-1) % self.x,
                            (pixel[0] - 1) // self.x)

    def mouse_interact_right(self, event):
        if event.widget.winfo_id() == self.canvas.winfo_id():
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)

            pixel = self.canvas.find_closest(x, y)
            self.canvas.itemconfig(pixel, fill="grey")
            self.drawer.erase((pixel[0]-1) % self.x,
                              (pixel[0] - 1) // self.x)

    def update_pixmap(self):
        for i in range(self.x * self.y):
            if self.canvas.itemcget(i+1, "fill") == "red":
                self.drawer.dot(i % self.x, i // self.x)
            else:
                self.drawer.erase(i % self.x, i // self.x)

        self.screen.refresh()


a = MatrixDrawer()
b = Updater(a)
thread1 = threading.Thread(target=b.toggle_livestream)
thread1.start()
a.root.mainloop()
b.livestream = False
