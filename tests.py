from libs.streamtools import Stream
from libs.image import Image
from libs.drawer import Drawer
from libs.screen import Screen
from libs.text import Text
from libs.slide import Slide
from libs.rainbow import msg, color

if __name__ == '__main__':
    scr = Screen(matrix=True, show=False, fps=60, tty='/dev/ttyACM0')
    aa = Text("the slide frame works!")
    slide = Slide(aa)
    scr.add(slide)

    while True:
        slide.refresh()
        scr.refresh()