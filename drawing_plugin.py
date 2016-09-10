#!/usr/bin/env python3

import tkinter
import threading
from tkinter import simpledialog
from copy import deepcopy
from libs.image import Image
from libs.drawer import Drawer
from libs.screen import Screen
from libs.text import Text

# TO DO LIST:
#       INSTRUCTIONS
#       CLICKING 2 DOTS AND THEN A LINE BETWEEN THEM APPEARS
#       CLICKING 2 DOTS AND A SQUARE BETWEEN THEM APPEARS
#       WRITING TEXT
#       SAVING / LOADING AN IMAGE
#       UNDO/REDO
#       PRESET ANIMATIONS


class Updater:
    """
    Class that simply serves to provide a live update to the matrix for the
    user drawing on the gui drawer
    """
    def __init__(self, interface):
        self.interface = interface
        self.screen = Screen(matrix=False, guishow=False, fps=50)
        self.screen.add(self.interface.image, refresh=False)

        self.live = False

    def one_refresh(self):
        self.screen.refresh()

    def toggle_live(self):
        while self.live:
            self.screen.refresh()



class MatrixDrawer:
    def __init__(self, x=64, y=16):
        self.image = Image(width=x, height=y)
        self.drawer = Drawer(self.image)
        self.updater = Updater(self)

        self.x = x
        self.y = y

        self.live = False
        self.drawmode = True
        self.updatethread = None
        self.textmode = False

        # Variables used for entry of text.
        self.savedtextpixmap = []
        self.lastpixel = (1,)

        self.create_window()
        self.create_canvas()
        self.create_buttons()
        self.create_mouse_binds()

        self.center(self.root)
        self.root.mainloop()    # Launch tkinter eventloop
        # This is run only after tkinter is closed and its event loop ends
        # Cleaning up any potential loose ends at close of program
        if self.updatethread is not None:
            self.updater.live = False
            self.updatethread.join()

    def center(self,window):
        """
        A magical function that centers the window in the middle of the screen
        """
        window.update_idletasks()
        width = window.winfo_width()
        frm_width = window.winfo_rootx() - window.winfo_x()
        win_width = width + 2 * frm_width
        height = window.winfo_height()
        titlebar_height = window.winfo_rooty() - window.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = window.winfo_screenwidth() // 2 - win_width // 2
        y = window.winfo_screenheight() // 2 - win_height // 2
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        window.deiconify()


    def create_mouse_binds(self):
        self.canvas.bind("<Button-1>", self.mouse_interact_left)
        self.canvas.bind("<B1-Motion>", self.mouse_interact_left)
        self.canvas.bind("<Button-3>", self.mouse_interact_right)
        self.canvas.bind("<B3-Motion>", self.mouse_interact_right)

    def create_window(self):
        self.root = tkinter.Tk()
        self.root.configure(bg="light blue")
        self.root.title("Matrix Drawer")

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
        self.updatebutton = tkinter.Button(self.buttonframe,
                                             text="Send To Matrix",
                                             bg="Yellow",
                                             command=self.updater.one_refresh
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
                                         command=self.toggledraw,
                                         text="Draw Mode",
                                         bg="Yellow",
                                         relief="sunken",
                                         activebackground="Yellow"
                                         )
        self.erasebutton = tkinter.Button(self.buttonframe,
                                          command=self.toggleerase,
                                          text="Erase Mode",
                                          bg="Grey",
                                          activebackground="Grey"
                                          )
        self.textbutton = tkinter.Button(self.buttonframe,
                                          command=self.toggletext,
                                          text="Enter Text",
                                          bg="Yellow",
                                          activebackground="Yellow"
                                          )
        self.updatebutton.grid(row=0, column=0, columnspan=2)
        self.clearbutton.grid(row=1, column=0, columnspan=2)
        self.fillbutton.grid(row=2, column=0, columnspan=2)
        self.livebutton.grid(row=3, column=0, columnspan=2)
        self.drawbutton.grid(row=4, column=0)
        self.erasebutton.grid(row=4, column=1)
        self.textbutton.grid(row=5, column=0, columnspan=2)

    def toggledraw(self):
        """
        Sets left mouse button to drawing
        """
        self.drawmode = True
        self.drawbutton.configure(relief="sunken",
                                  bg="Yellow",
                                  activebackground="Yellow")
        self.erasebutton.configure(relief="raised",
                                   bg="Grey",
                                   activebackground="Grey")

    def toggleerase(self):
        """
        Sets left mouse button to erasing
        """
        self.drawmode = False
        self.drawbutton.configure(relief="raised",
                                  bg="Grey",
                                  activebackground="Grey")
        self.erasebutton.configure(relief="sunken",
                                   bg="Yellow",
                                   activebackground="Yellow")

    def togglelive(self):
        """
        Creates new thread and launches permanent loop to keep matrix updated
        in real time
        """
        if self.updater.live:   # we were already live, going manual now
            self.livebutton.configure(text="Status: Manual")
            # Stop the infinite loop in the other thread and terminate it
            self.updater.live = False
            self.updatethread.join()
            self.updatethread = None

        else:           # we were manual, now going live
            self.livebutton.configure(text="Status: Live")
            self.updater.live = True
            # Open a new thread and launch the infinite update loop
            self.updatethread = threading.Thread(target=self.updater.toggle_live)
            self.updatethread.start()

    def confirmtext(self, event):
        self.create_mouse_binds()
        self.canvas.unbind("<Motion>")
        for button in self.buttonframe.children.values():
            button.configure(state="normal")

    def toggletext(self):
        text = simpledialog.askstring("ENTER THE TEXT", "PLEASE")
        if text is not None:
            self.textimage = Text(text=text)
            self.canvas.bind("<Button-1>", self.confirmtext)
            self.canvas.bind("<Motion>", self.mouse_interact_movement)

            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<Button-3>")
            self.canvas.unbind("<B3-Motion>")
            self.savedtextpixmap = deepcopy(self.image.pixmap)

            for button in self.buttonframe.children.values():
                button.configure(state="disabled")

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
        """
        Left mouse's function depends on the 2 draw/erase buttons available to
        the user
        """
        x = event.x
        y = event.y

        pixel = self.canvas.find_closest(x, y)
        if self.drawmode:
            self.canvas.itemconfig(pixel, fill="red")
            self.drawer.dot((pixel[0]-1) % self.x,
                            (pixel[0] - 1) // self.x)

        else:
            self.canvas.itemconfig(pixel, fill="grey")
            self.drawer.erase((pixel[0]-1) % self.x,
                            (pixel[0] - 1) // self.x)

    def mouse_interact_right(self, event):
        """
        Right mouse button always used for erasing
        """
        x = event.x
        y = event.y

        pixel = self.canvas.find_closest(x, y)
        self.canvas.itemconfig(pixel, fill="grey")
        self.drawer.erase((pixel[0]-1) % self.x,
                          (pixel[0] - 1) // self.x)

    def mouse_interact_movement(self, event):
        if not self.textmode:
            x = event.x
            y = event.y
            pixel = self.canvas.find_closest(x, y)

            if pixel != self.lastpixel:
                self.lastpixel = pixel
                self.image.pixmap = deepcopy(self.savedtextpixmap)
                self.image.paste(self.textimage, mode="fill", x=(pixel[0]-1) % self.x, y=(pixel[0]-1) // self.x)
                self.update_gui_from_pixmap()

    def update_gui_from_pixmap(self):
        for y in range(self.y):
            for x in range(self.x):
                if self.image.get_pixmap()[y][x]:
                    self.canvas.itemconfig(y*64+x+1, fill="red")
                else:
                    self.canvas.itemconfig(y*64+x+1, fill="grey")


if __name__ == '__main__':
    MatrixDrawer()
