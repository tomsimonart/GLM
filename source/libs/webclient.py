#!/usr/bin/env python3

import json
import queue
import socket
import signal
import threading
import traceback
from time import sleep
from ..libs.rainbow import msg

BUFFSIZE = 512


class WebClient():
    def __init__(self, data, queue_, server_ip="localhost", server_port=9999):
        super(WebClient, self).__init__()
        self.server_ip = server_ip
        self.server_port = server_port

        self.connected = False
        self.exit = False

        self.end = queue_
        self.data = data
        self.events = queue.Queue()

    def close_connection(self, signum, frame):
        msg("killed", 3)
        self.kill = True

    def is_connected(self):
        return self.connected

    def _get_data(self):
        """ Get web data from plugin in encoded json format
        """
        return json.dumps(self.data).encode()

    def get_event(self):
        """ Send event to plugin if there is one, otherwise None
        """
        try:
            event = self.events.get(block=False)
            return event
        except queue.Empty:
            return None

    def check_exit(self):
        exit = self.end.get(False)
        if exit == "END":
            self.exit = True

    def _get_event_loop(self, user):
        """ Threaded event receive
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server_ip, self.server_port))
        self.client.send(user.encode())

        status = self.client.recv(BUFFSIZE).decode()
        if status == "a:client_connected":
            self.connected = True

            while self.connected:
                self.client.send(b"READY")

                # Receive event
                event_json = self.client.recv(BUFFSIZE).decode()
                if not event_json:
                    self.connected = False

                else:
                    event = json.loads(event_json)

                    # refresh phase
                    if event == "REFRESH":
                        self.client.send(self._get_data())

                    # event phase
                    elif type(event) == dict:
                        self.client.send(json.dumps("RECEIVED").encode())

                    # unknown phase
                    elif event == "UNKNOWN":
                        self.client.send(json.dumps("RETRYING").encode())


        # self.connected = True
        # msg("Connected", 1, "Thread")
        #
        # self.client.send(user.encode()) # Send user name
        # status = self.client.recv(BUFFSIZE).decode()
        #
        # msg("Connected")
        #
        # if status == "a:client_connected":
        #     while True:
        #         msg("Working", 3)
        #         # Check if plugin has been killed
        #
        #         self.check_exit()
        #         if self.exit:
        #             self.client.send(b"EOT")
        #             msg("stopping", 2, "Thread")
        #             msg("killed", 3, "Process")
        #             self.client.close()
        #             self.connected = False
        #             break
        #
        #         else:
        #             # Still connected header
        #             self.client.send("READY".encode())
        #             # Get event
        #             r = self.client.recv(BUFFSIZE).decode()
        #             event = json.loads(r)
        #             msg(event, 3)
        #             self.events.put(event) # Add the event in the event queue
        #             msg("receive", 0, "plugin_handler", event)
        #             # Send data back
        #             if event["method"] == "GET":
        #                 if event["data"] == "refresh":
        #                     msg("sent " + self._get_data().decode())
        #                     self.client.send(self._get_data())
        #                     # msg("send", 0, "plugin_handler", self._get_data())
        #
        # else:
        #     msg("Connection refused", 3)

    def handle_data(self, user="plugin"):
        """ Change handle_data name
        """
        if not self.connected and not self.exit:
            get_event = threading.Thread(
                target=self._get_event_loop,
                args=(user,),
                daemon=True
                )
            get_event.start()
            msg("starting", 1, "Thread")
