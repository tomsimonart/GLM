import queue
from time import sleep
from ..libs.screen import Screen
from ..libs.slide import *
from ..libs.text import Text
from ..libs.webclient import WebClient
from ..libs.rainbow import msg
import signal

class Plugin():
    def __init__(self, process_events, start, matrix, show, guishow):
        super(Plugin, self).__init__()
        self.name = "Example Plugin"
        self.version = "0.0.3"
        self.author = "Infected"

        if start:
            self.process_events = process_events

            self.sample_text = Text('bitconneeeeect')
            self.slide = Slide(self.sample_text)

            self.screen = Screen(
                matrix=matrix,
                show=show,
                guishow=guishow,
                fps=5
                )
            self.screen.add(self.slide, refresh=True, x=1, y=0)

            self.data = [
                ("a_0", "<a href='google.com'>google</a>"),
                ("button_0" ,"<button>ok</button>")
                ]
            self.client = WebClient(self.data, process_events)
            self._start()

    def _start(self):
        msg("STARTING PLUGIN", level=1)
        while True:
            if not self.client.is_connected():
                self.client.handle_data()
            if self.client.check_exit():
                msg("ENDING PLUGIN", 3, level=1)
                break
            self.slide.refresh('down', 8, 1)
            self.screen.refresh()
