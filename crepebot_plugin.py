#!/usr/bin/env python3
# Crepe bot plugin by infected

from libs.streamtools import Stream
from libs.text import Text
from libs.image import Image
from libs import pbmtools

from os import environ
#from twisted.internet.defer import inlineCallbacks
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner

class CrepeBot(ApplicationSession):
    def __init__(self, *args,**kwargs):
        super(CrepeBot, self).__init__(*args, **kwargs)
        self.pbm = Image()
        self.bar = Image()
        self.bar_x = 40
        self.bar_y = 7
        self.image = Image()
        self.stream = Stream(matrix=True)

    @coroutine
    def onJoin(self, details):
        def onRefresh(*queue):
            try:
                self.refresh(queue[0]['percent'], queue[0]['name'])
            except ValueError as e:
                print(e)
            except IndexError as e:
                print(e)
            print(queue)

        self.subscribe(onRefresh, 'queue')

    def refresh(self, percentage, name):
        self.splash = Text(str(name).lower())
        self.image.blank()
        self.bar.blank()
        self.image.paste(self.splash, x=25, y=0)
        self.refresh_bar(percentage)
        self.image.paste(self.bar.get_pixmap(), x=self.bar_x, y=self.bar_y)
        self.percentage_text = Text(str(percentage) + '%')
        self.image.paste(self.percentage_text, x=40, y=10)
        self.stream.set_data_from_matrix(self.image.get_pixmap())
        self.stream.send_to_serial()
        #print(self.stream)

    def refresh_bar(self, percentage):
        self.bar.draw_line(x1=0, y1=0, x2=percentage // 5, y2=0)
        self.bar.draw_line(x1=0, y1=1, x2=percentage // 5, y2=1)

if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://titoubuntu:8080/ws"),
        u"crepinator"
        )
    runner.run(CrepeBot)
