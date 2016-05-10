from libs.streamtools import Stream
from libs.image import Image
from libs.rainbow import color, msg
from os import system
from time import sleep
from sys import argv

MAT_WIDTH = 64
MAT_HEIGHT = 16


class Screen:
    """
    Screen is the Image manager for the plugins.
    Each child of it is an Image and can be added with the 'add' method.
    On each 'refresh' all the images are flattened to one Image and sent to
    the streamer

    Screen must have the same size of the matrix

    Keyword arguments:
    x -- x height (default MAT_HEIGHT)
    y -- y width (default MAT_WIDTH)
    matrix -- output to serial (default True)
    show -- verbose output (default False)
    fps -- not implemented (default 0)
    """
    def __init__(
            self,
            width=MAT_WIDTH,
            height=MAT_HEIGHT,
            matrix=True,
            show=False,
            fps=0):

        if fps > 0:
            self.fps = 1 / fps
        else:
            self.fps = 0
        self.image = Image(width=width, height=height)
        self.streamer = Stream(matrix=matrix)
        self.show = show
        self.childs = []

    def add(self, image, x=0, y=0, refresh=True, mode="fill", name="Child"):
        """
        Add a new Image to the childs.

        Keyword arguments:
        image -- Image
        x -- x paste location (default 0)
        y -- y paste location (default 0)
        refresh -- blank Image after refresh (default True)
        mode -- paste mode [Image.paste()] (default "fill")
        name -- name (default "Child")
        """
        self.childs.append((image, x, y, refresh, mode, name))

    def remove(self, id_):
        """Delete a child by his id"""
        if id_ <= len(self.childs) - 1:
            msg(self.childs.pop(id_)[5], 0, "Removed")
        else:
            msg("no such child", 2, "Screen.remove()", len(self.childs), id_)


    def refresh(self):
        """
        Flatten all childs into one Image and send it to the streamer
        and/or print it in the terminal.
        """
        self.image.blank()
        for child in self.childs:
            self.image.paste(child[0], x=child[1], y=child[2], mode=child[4])

            # Refresh
            if child[3]:
                child[0].blank()

        self.streamer.set_data(self.image)
        self.streamer.send_to_serial()
        if self.show:
            system('clear')
            print(self.streamer)
        sleep(self.fps)

    def __str__(self):
        count = len(self.childs) - 1
        string = color("Screen", "green") + "\n"
        for n, child in enumerate(self.childs):
            if n < count:
                string += color('├─', 'blue')
            else:
                string += color('└─', 'blue')

            string += color(str(n), 'red')
            string += color("..", 'yellow')
            string += color(child[5], 'green', False, None, "Underline")
            if child[3]:
                string += "[" + color("1", "magenta", False) + "]"
            else:
                string += "[" + color("O", "magenta", False) + "]"
            string += "\n"
        return string
