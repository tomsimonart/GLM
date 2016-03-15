#!/usr/bin/env python3

import tkinter

# CLEAR BUTTON
# INSTRUCTIONS
# FILL ALL BUTTON


class MatrixDrawer:
    def __init__(self, x=64, y=16):
        self.root = tkinter.Tk()
        self.root.configure(bg="light blue")
        self.pixmap = [[0 for x in range(x)] for y in range(y)]
        self.x = x
        self.y = y

        self.create_canvas()

        self.root.bind("<Button-1>", self.mouseinteract1)
        self.root.bind("<B1-Motion>", self.mouseinteract2)
        self.root.bind("<Button-3>", self.mouseinteract3)
        self.root.bind("<B3-Motion>", self.mouseinteract3)

        self.create_buttons()

    def create_canvas(self):
        self.canvasframe = tkinter.Frame(self.root)
        self.canvasframe.pack(side="right")
        square_size = 22
        self.canvas = tkinter.Canvas(self.canvasframe, bg="yellow",
                                     height=len(self.pixmap)*square_size,
                                     width=len(self.pixmap[1])*square_size)

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
        self.terminalbutton.grid(row=0, column=0)

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
                self.pixmap[i // 64][i % 64] = 1

        for elem in self.pixmap:
            print(elem)

a = MatrixDrawer()
a.root.mainloop()
