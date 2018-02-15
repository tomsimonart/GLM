from ..libs.screen import Screen
from ..libs.text import Text
from ..libs.webframe import Webframe

class Plugin():
    def __init__(self, matrix=True, show=False, guishow=False):
        super(Plugin, self).__init__()
        self.name = "Example Plugin"
        self.version = "0.0.3"

        self.sample_text = Text('sample text')

        self.screen = Screen(matrix=matrix, show=show)
        self.screen.add(self.sample_text, refresh=False)

        self.interface = Webframe()

    def start(self):
        self.screen.refresh()
