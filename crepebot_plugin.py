#!/usr/bin/env python3
# Crepe bot plugin by infected

from libs.screen import Screen
from libs.text import Text
from libs.image import Image
from libs import pbmtools

from os import environ
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner

class CrepeBot(ApplicationSession):
    def __init__(self, *args,**kwargs):
        super(CrepeBot, self).__init__(*args, **kwargs)
        self.screen = Screen(matrix=True, show=True)
        self.pbm = Image()
        self.bar = Image()
        self.splash = Text('init v1.0')
        self.percentage_text = Text('0')
        self.bar_x = 40
        self.bar_y = 7

        self.screen.add(self.pbm, 0, 0, False)
        self.screen.add(self.bar, self.bar_x, self.bar_y, True)
        self.screen.add(self.splash, 25, 0, True)
        self.screen.add(self.percentage_text, 40, 10, True)

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
        self.splash.edit(str(name).lower)
        self.refresh_bar(percentage)
        self.percentage_text.edit(str(percentage) + '%')
        self.screen.refresh()

    def refresh_bar(self, percentage):
        self.bar.draw_line(x1=0, y1=0, x2=percentage // 5, y2=0)
        self.bar.draw_line(x1=0, y1=1, x2=percentage // 5, y2=1)

if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://titoubuntu:8080/ws"),
        u"crepinator"
        )
    runner.run(CrepeBot)
