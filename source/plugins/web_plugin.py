import queue
from time import sleep
from ..libs.screen import Screen
from ..libs.text import Text
from ..libs.webclient import WebClient
from ..libs.rainbow import msg
import signal

class Plugin():
    def __init__(
        self,
        process_events,
        start,
        matrix=True,
        show=False,
        guishow=False
        ):
        super(Plugin, self).__init__()

        self.process_events = process_events

        self.name = "Example Plugin"
        self.version = "0.0.3"

        self.sample_text = Text('web plugin')

        self.screen = Screen(matrix=matrix, show=show)
        self.screen.add(self.sample_text, refresh=False, x=9, y=4)

        self.data = ["<a href='google.com'>google</a>","<button>ok</button>"]
        self.client = WebClient(self.data, process_events)

        if start:
            self._start()

    def _start(self):
        event = self.client.get_event()
        if event is not None:
            # Execute event
            pass
        if not self.client.is_connected():
            self.client.handle_data()
        while True:
            if self.client.check_exit():
                msg("ENDING PLUGIN", 3)
                break
            msg("REFRESHED")
            sleep(3)
