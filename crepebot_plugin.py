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
        self.percentage = 0
        self.percentage_text = Text(str(self.percentage))
        self.pbm = Image()
        self.bar = Image()
        self.bar_x = 40
        self.bar_y = 7
        self.image = Image()
        self.stream = Stream(matrix=True)
        self.splash = Text('crèpe bot')

    @coroutine
    def onJoin(self, details):
        def onRefresh(queue):
            print(queue)

        self.subscribe(onRefresh, 'queue')

    def refresh(self, percentage):
        self.percentage = percentage
        self.percentage_text = Text(str(percentage)+'%')
        self.image.blank()
        self.image.paste(self.splash.get_text(), x=25, y=0)
        self.refresh_bar(percentage)
        self.image.paste(self.bar.get_pixmap(), x=self.bar_x, y=self.bar_y)
        self.image.paste(self.percentage_text.get_text(), x=40, y=10)

        self.stream.set_data_from_matrix(self.image.get_pixmap())
        self.stream.send_to_serial()
        #print(self.stream)

    def refresh_bar(self, percentage):
        if percentage % 5 == 0:
            self.bar.draw_dot(x=0 + percentage // 5, y=0)
            self.bar.draw_dot(x=0 + percentage // 5, y=1)

if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://10.0.0.1:8080/ws"),
        u"crepinator"
        #debug=False  # optional; log even more details
        )
    runner.run(CrepeBot)
