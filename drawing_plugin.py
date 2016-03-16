#!/usr/bin/env python3

import tkinter
from libs.image import Image
from libs.drawer import Drawer
from libs.screen import Screen

# INSTRUCTIONS
# DIFFERENT BRUSHES
# CLICKING 2 DOTS AND THEN A LINE BETWEEN THEM APPEARS
# CLICKING 2 DOTS AND A SQUARE BETWEEN THEM APPEARS
# LIVE UPDATING


class MatrixDrawer:
    def __init__(self, x=64, y=16):
        self.image = Image(width=x, height=y)
        self.drawer = Drawer(self.image)
        self.screen = Screen(matrix=True, show=True)
        self.screen.add(self.image)

        self.x = x
        self.y = y

        self.create_window()
        self.create_canvas()
        self.create_buttons()

    def create_window(self):
        self.root = tkinter.Tk()
        self.root.configure(bg="light blue")

        self.root.bind("<Button-1>", self.mouseinteract1)
        self.root.bind("<B1-Motion>", self.mouseinteract2)
        self.root.bind("<Button-3>", self.mouseinteract3)
        self.root.bind("<B3-Motion>", self.mouseinteract3)

    def create_canvas(self):
        self.canvasframe = tkinter.Frame(self.root)
        self.canvasframe.pack(side="right")
        square_size = 22
        self.canvas = tkinter.Canvas(self.canvasframe, bg="yellow",
                                     height=self.y*square_size,
                                     width=self.x*square_size)

        self.canvas.grid(row=0, column=0)

        for y in range(self.y):
            for x in range(self.x):
                self.canvas.create_rectangle(x*square_size, y*square_size,
                                             x*square_size + square_size,
                                             y*square_size + square_size,
                                             fill="grey")

    def create_buttons(self):
        self.buttonframe = tkinter.Frame(self.root)
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

        self.terminalbutton.grid(row=0, column=0)
        self.clearbutton.grid(row=1, column=0)
        self.fillbutton.grid(row=2, column=0)

    def clearall(self):
        """
        Clears all squares, resetting them back to grey
        """
        for i in range(self.x * self.y):
            self.canvas.itemconfig(i+1, fill="grey")

    def fillall(self):
        """
        Fills all squares, setting them to red
        """
        for i in range(self.x * self.y):
            self.canvas.itemconfig(i+1, fill="red")

    def mouseinteract1(self, event):
        """
        For Left-click
        Write/Erase
        """
        if event.widget.winfo_id() == self.canvas.winfo_id():
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)

            square = self.canvas.find_closest(x, y)

            if self.canvas.itemcget(square, "fill") == "grey":
                self.canvas.itemconfig(square, fill="red")
            else:
                self.canvas.itemconfig(square, fill="grey")

    def mouseinteract2(self, event):
        """
        For Left-Drag
        Write
        """
        if event.widget.winfo_id() == self.canvas.winfo_id():
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)

            square = self.canvas.find_closest(x, y)
            self.canvas.itemconfig(square, fill="red")

    def mouseinteract3(self, event):
        """
        For Right-click / Right-Drag
        Erase
        """
        if event.widget.winfo_id() == self.canvas.winfo_id():
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)

            square = self.canvas.find_closest(x, y)
            self.canvas.itemconfig(square, fill="grey")

    def update_pixmap(self):
        for i in range(self.x * self.y):
            if self.canvas.itemcget(i+1, "fill") == "red":
                self.drawer.dot(i % self.x, i // self.x)
            else:
                self.drawer.erase(i % self.x, i // self.x)

        self.screen.refresh()

a = MatrixDrawer()
a.root.mainloop()
