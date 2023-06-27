#!/usr/bin/env python

import time
import socket
import math
import logging

class Send_socket():

    def __init__(self, ip_address) -> None:
        self.host = ip_address
        self.port = 30001

        logging.basicConfig(level=logging.INFO)

    def connect(self) -> None:
        self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.con.connect((self.host, self.port))


    def send(self, action):
        self.con.send((f"movel(p{action}, a=0.01, v=0.05)"+"\n").encode('utf8'))
        time.sleep(1)

    def disconnect(self):
        self.con.close()