#!/usr/bin/env python3

import json
import queue
import socket
import signal
import threading
from time import sleep
from ..libs.rainbow import msg

BUFFSIZE = 512


class WebClient():
    def __init__(self, data, server_ip="localhost", server_port=9999):
        super(WebClient, self).__init__()
        self.server_port = server_port
        self.server_ip = server_ip

        # Catch process closing
        signal.signal(signal.SIGTERM, self.close_connection)
        self.kill = False

        self.connected = False

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server_ip, server_port))

        self.data = data
        self.events = queue.Queue()

    def close_connection(self, signum, frame):
        self.kill = True

    def is_connected(self):
        return self.connected

    def _get_data(self):
        """ Get web data from plugin in encoded json format
        """
        print(self.data)
        return json.dumps(self.data).encode()

    def get_event(self):
        """ Send event to plugin if there is one, otherwise None
        """
        try:
            event = self.events.get(block=False)
            return event
        except queue.Empty:
            return None

    def _get_event_loop(self, user):
        """ Threaded event receive
        """
        self.client.send(user.encode()) # Send user name
        response = self.client.recv(BUFFSIZE).decode()
        msg("Connected")

        if response == "a:client_connected":
            while not self.kill:
                msg("Working", 3)
                # Check if plugin has been killed
                if self.kill:
                    # Sending end signal to server
                    self.client.settimeout(3)
                    trash = self.client.recv(BUFFSIZE) # get trash data
                    self.client.settimeout(None)
                    self.client.send(json.dumps("EOT").encode())
                    msg("stopping", 2, "Thread")
                    msg("killed", 3, "Process")
                    self.client.close()
                    self.connected = False
                    break

                else:
                    # Still connected header
                    self.client.send(json.dumps("READY").encode())
                    # Get event
                    r = self.client.recv(BUFFSIZE).decode()
                    event = json.loads(r)
                    msg(event, 3)
                    self.events.put(event) # Add the event in the event queue
                    msg("receive", 0, "plugin_handler", event)
                    # Send data back
                    if event["method"] == "GET":
                        if event["data"] == "refresh":
                            msg("sent " + self._get_data().decode())
                            self.client.send(self._get_data())
                            # msg("send", 0, "plugin_handler", self._get_data())

        else:
            msg("Connection refused", 3)

    def handle_data(self, user="plugin"):
        """ Change handle_data name
        """
        if not self.connected:
            get_event = threading.Thread(
                target=self._get_event_loop,
                args=(user,),
                daemon=True
                )
            get_event.start()
            self.connected = True
            msg("starting", 0, "Thread")
