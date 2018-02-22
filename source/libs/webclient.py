#!/usr/bin/env python3

import json
import socket
import signal
import threading
from time import sleep
from ..libs.rainbow import msg

BUFFSIZE = 512


class WebClient():
    def __init__(self, server_ip="localhost", server_port=9999):
        super(WebClient, self).__init__()
        self.server_port = server_port
        self.server_ip = server_ip

        # Catch process closing
        signal.signal(signal.SIGTERM, self.close_connection)
        self.kill = False

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server_ip, server_port))

        self.data = ["<a href='google.com'>google</a>","<button>ok</button>"]

    def close_connection(self, signum, frame):
        self.kill = True

    def _get_data(self):
        """ Get web data from plugin
        """
        pass

    def _send_event(self):
        """ Send event to plugin
        """
        pass

    def handle_data(self, user="plugin", data=" "):
        """ Change handle_data name
        """
        self.client.send(user.encode()) # Send user name
        response = self.client.recv(BUFFSIZE).decode()
        msg(response, 0, "plugin_handler")

        if response == "a:client_connected":
            while not self.kill:
                if self.kill:
                    msg("killed", 3, "Process")
                    self.client.send(b"EOT") # Sending end signal
                    self.client.close()
                else:
                    # Get event
                    event = json.loads(self.client.recv(BUFFSIZE).decode())
                    msg("event", 0, "plugin_handler", event)
                    # Send data back
                    self.client.send(json.dumps(self.data).encode())
                    msg("data", 0, "plugin_handler", self.data)

        else:
            msg("Connection refused", 3)
