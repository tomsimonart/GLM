#!/usr/bin/env python3

import tkinter
from libs.image import Image
from libs.drawer import Drawer
from libs.screen import Screen

# INSTRUCTIONS
# DIFFERENT BRUSHES
# CLICKING 2 DOTS AND THEN A LINE BETWEEN THEM APPEARS
# CLICKING 2 DOTS AND A pixel BETWEEN THEM APPEARS
# WRITING TEXT


class MatrixDrawer:
    def __init__(self, x=64, y=16):
        self.image = Image(width=x, height=y)
        self.drawer = Drawer(self.image)
        self.screen = Screen(matrix=True, show=True, fps=50)
        self.screen.add(self.image, refresh=False)

        self.x = x
        self.y = y
        self.live = False

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
        pixel_size = 22
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

        self.terminalbutton.grid(row=0, column=0, columnspan=3)
        self.clearbutton.grid(row=1, column=0, columnspan=3)
        self.fillbutton.grid(row=2, column=0, columnspan=3)
        self.livebutton.grid(row=3, column=0, columnspan=3)

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
            self.root.after(50, self.live_update)

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

    def mouseinteract1(self, event):
        """
        For Left-click
        Write/Erase
        """
        if event.widget.winfo_id() == self.canvas.winfo_id():
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)

            pixel = self.canvas.find_closest(x, y)

            if self.canvas.itemcget(pixel, "fill") == "grey":
                self.canvas.itemconfig(pixel, fill="red")
                self.drawer.dot((pixel[0]-1) % self.x, (pixel[0] - 1) // self.x)
            else:
                self.canvas.itemconfig(pixel, fill="grey")
                self.drawer.erase((pixel[0]-1) % self.x, (pixel[0] - 1) // self.x)

    def mouseinteract2(self, event):
        """
        For Left-Drag
        Write
        """
        if event.widget.winfo_id() == self.canvas.winfo_id():
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)

            pixel = self.canvas.find_closest(x, y)
            self.canvas.itemconfig(pixel, fill="red")
            self.drawer.dot((pixel[0]-1) % self.x, (pixel[0] - 1) // self.x)

    def mouseinteract3(self, event):
        """
        For Right-click / Right-Drag
        Erase
        """
        if event.widget.winfo_id() == self.canvas.winfo_id():
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)

            pixel = self.canvas.find_closest(x, y)
            self.canvas.itemconfig(pixel, fill="grey")
            self.drawer.erase((pixel[0]-1) % self.x, (pixel[0] - 1) // self.x)

    def update_pixmap(self):
        for i in range(self.x * self.y):
            if self.canvas.itemcget(i+1, "fill") == "red":
                self.drawer.dot(i % self.x, i // self.x)
            else:
                self.drawer.erase(i % self.x, i // self.x)

        self.screen.refresh()

a = MatrixDrawer()
a.root.mainloop()
