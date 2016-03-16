from libs.streamtools import Stream

class Screen:
    def __init__(self, image, x=0, y=0, matrix=True, show=False):
        self.image = image
        self.streamer = Stream(matrix=matrix)
        self.show = show
        self.childs = []

    def add(self, image, x=0, y=0, refresh=True):
        self.childs.append((image, x, y, refresh))

    def refresh(self):
        self.image.blank()
        for screen in self.childs:
            self.image.paste(screen[0], x=screen[1], y=screen[2])
            if screen[3]:
                screen[0].blank()
        self.streamer.set_data(self.image)
        self.streamer.send_to_serial()
        if self.show:
            print(self.streamer)
