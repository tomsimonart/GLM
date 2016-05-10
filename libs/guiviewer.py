import tkinter
import threading
import time
from libs.image import Image
from libs.drawer import Drawer

class GuiViewer:
    def __init__(self, image):
        self.image = image
        self.drawer = Drawer(self.image)

        self.x = self.image.width
        self.y = self.image.height

        self.create_window()
        self.create_canvas()

        self.update_pixmap()    #Most important function

        self.root.mainloop()

    def create_window(self):
        self.root = tkinter.Tk()
        self.root.configure(bg="light blue")

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

    def update_pixmap(self):
        """
        Runs after every turn of the mainloop updating the matrix.
        Kind of infinite until end of life of the tkinter gui.
        """
        for i in range(len(self.image.pixmap)):
            for j in range(len(self.image.pixmap[i])):
                if self.image.pixmap[i][j] == 1:
                    self.canvas.itemconfigure(i*self.x + j + 1, fill="red")
                else:
                    self.canvas.itemconfigure(i*self.x + j + 1, fill="grey")
        self.root.after(50, self.update_pixmap)
