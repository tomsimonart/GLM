from ..libs.screen import Screen
from ..libs.text import Text
from ..libs.webclient import WebClient

class Plugin():
    def __init__(self, matrix=True, show=False, guishow=False):
        super(Plugin, self).__init__()
        self.name = "Example Plugin"
        self.version = "0.0.3"

        self.sample_text = Text('web plugin')

        self.screen = Screen(matrix=matrix, show=show)
        self.screen.add(self.sample_text, refresh=False, x=9, y=4)

        self.interface = WebClient()

    def start(self):
        self.interface.send_data()
        self.screen.refresh()

    def get_interface(self):
        return "<input></input><button>test</button>"
