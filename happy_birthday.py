from libs.screen import Screen
from libs.image import Image
from libs.rainbow import color, msg
from libs.text import Text
from libs.drawer import Drawer

class Hbd_plugin:
    def __init__(self):
        msg("input()", 2, "Hbd_plugin.__init__()")
        self.name_text = input(color("Enter name: ", "yellow")).lower()

        self.mask = Image(64,16)
        self.mask.fill()

        self.bg = Image(64, 16)
        self.drawer = Drawer(self.bg)
        self.drawer.dot(0, 0)
        self.drawer.dot(0, 15)
        self.drawer.dot(63, 0)
        self.drawer.dot(63, 15)

        self.label = Text(text="° bon annif! °")
        self.name = Text(text=self.name_text)

        self.screen = Screen(matrix=False, show=True, fps=1.7)

        self.screen.add(self.bg, refresh=False)
        self.screen.add(self.label, x=2, y=2, refresh=False)
        xloc = (64 - abs(self.name.width)) // 2
        self.screen.add(self.name, x=xloc, y=8, refresh=False)
        self.screen.add(self.mask, refresh=False, mode="invert")

    def stream(self):
        try:
            blink = False
            while True:
                blink = not blink
                if blink:
                    self.mask.blank()
                else:
                    self.mask.fill()

                self.screen.refresh()
        except KeyboardInterrupt:
            print()
            msg(self.name_text, 0, "output")
            exit()


if __name__ == '__main__':
    plugin = Hbd_plugin()
    plugin.stream()