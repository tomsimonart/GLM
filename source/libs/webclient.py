#!/usr/bin/env python3

import socket
import signal
from time import sleep
from ..libs.rainbow import msg

BUFFSIZE = 512


class WebClient():
    def __init__(self, server_ip="localhost", server_port=9999):
        super(WebClient, self).__init__()
        self.server_port = server_port
        self.server_ip = server_ip
        self.kill = False

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server_ip, server_port))

    def send_data(self, user="plugin", data=" "):
        connected = False
        failed = False
        while not connected and not failed:
            self.client.send(user.encode()) # 1 send (user name)
            server_recv = self.client.recv(BUFFSIZE).decode()
            if server_recv == "a:client_connected":
                # Client connected
                connected = True
                msg("Connected", 0, "send_data", server_recv)
                self.client.send("data".encode()) # 2 send data

            elif server_recv == "e:bad_user":
                # Failed to connect
                msg("Failed to connect", 2, "send_data", server_recv)
                failed = True

            else:
                # Failed to connect
                msg("No connection, trying again...", 2)
                sleep(1)

        if connected:
            # async send recv
            ans = self.client.recv(BUFFSIZE)
            msg(ans.decode(), 0, "server")

        msg("Closing socket", 1)
        self.client.close()
