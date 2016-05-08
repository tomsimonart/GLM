from libs.streamtools import Stream
from libs.image import Image
from libs.drawer import Drawer
from libs.screen import Screen
from libs.text import Text
from libs.rainbow import msg, color

if __name__ == '__main__':
    scr = Screen(matrix=False, show=True)

    a = Image(64, 16)
    b = Image(64, 2)
    c = Image(width=2, height=2, pixmap=[[1, 0, 1], [0, 1, 0], [1, 0, 1]])
    b.fill()
    scr.add(a, name="Background")
    scr.add(b, name="Stripe", refresh=False)
    scr.add(c, name='cross', x=31, y=7, refresh=False)
    scr.refresh()
    print(scr)
    msg("done", 0, "tests.py")
    print(c)
    c.resize(4, 7)
    print(c.pixmap)

    a.set_pixmap([2])
    print(a)
