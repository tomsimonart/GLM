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
        self.name = "Template Plugin"
        self.version = "0.0.3"
        self.author = "Infected"

        if start: # If start is True
            # Required
            self.process_events = process_events # Event queue
            self.screen = Screen( # Create matrix screen
                matrix=matrix,
                show=show,
                guishow=guishow,
                fps=0.333
            )
            self.data = """
            {{ 'input label'|input }}
            {{ 'button label'|button }}
            """ # Templated data
            # TODO untemplate data to webclient
            # Initialize web client
            self.client = WebClient(self.data, process_events)
            self.make_layout() # Create screen layout
            self._start() # Start plugin loop


    def make_layout(self):
        self.sample_text = Text('example')
        self.screen.add(self.sample_text, refresh=False, x=6, y=7)


    def _start(self):
        # Plugin loop
        msg("STARTING PLUGIN", level=1)
        loop = True
        while loop:
            if not self.client.is_connected(): # Connect or reconnect
                self.client.handle_data() # Start self.client

            if self.client.check_exit():
                msg("ENDING PLUGIN", 3, level=1)
                loop = False
            else:
                # Plugin loop
                event = self.client.get_event() # Get events (non blocking)
                self.screen.refresh()
