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
    def __init__(
            self,
            data,
            process_events,
            server_ip="localhost",
            server_port=9999
            ):
        super(WebClient, self).__init__()
        self.server_ip = server_ip
        self.server_port = server_port

        self.connected = False
        self.exit = False

        self.process_events = process_events
        self.data = data
        self.events = queue.Queue()

    def _set_connected(self, connected):
        self.connected = connected

    def is_connected(self):
        return self.connected

    def _close_connection(self):
        self._set_connected(False)
        self.client.send(b"EOT")
        self.client.close()

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
        try:
            exit = self.process_events.get(False)
        except queue.Empty:
            exit = False
        if exit == "END":
            self.exit = True
        return self.exit

    def _get_event_loop(self, user):
        """ Threaded event receive
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((self.server_ip, self.server_port))
        except socket.error as error:
            if error.errno == socket.errno.ECONNREFUSED:
                status = "e:refused"
                msg("refused", 3)
        self.client.send(user.encode())

        status = self.client.recv(BUFFSIZE).decode()
        if status == "a:client_connected":
            self.connected = True

            while self.is_connected():
                self.client.send(b"READY")

                if self.check_exit():
                    trash = self.client.recv(BUFFSIZE).decode()
                    self._close_connection()

                else:
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
