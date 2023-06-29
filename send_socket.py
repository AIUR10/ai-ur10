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


    def send_circular_action(self, current_position, receiver, shared_variable):

        first_pose_via = current_position.copy()
        first_pose_via[1] -= 0.35
        first_pose_via[2] += 0.35

        first_pose_to = current_position.copy()
        first_pose_to[1] -= 0.7

        self.con.send((f"movec(p{first_pose_via}, p{first_pose_to}, a=0.01,v=0.1,r=0,mode=1)"+"\n").encode('utf8'))

        time.sleep(20)

        receiver.receive()

        with shared_variable.get_lock():
            shared_variable.value = True

        second_pose_via = first_pose_via.copy()
        second_pose_to = current_position.copy()

        self.con.send((f"movec(p{second_pose_via}, p{second_pose_to}, a=0.01,v=0.1,r=0,mode=1)"+"\n").encode('utf8'))

        time.sleep(20)

    def disconnect(self):
        try:
            self.con.close()
        except:
            pass
        finally:
            pass