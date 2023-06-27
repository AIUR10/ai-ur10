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

        joint_positions_radians = [math.radians(joint_position_degree) for joint_position_degree in action]

        self.con.send((f"movec(p[2.59531298e-02, -5.51968548e-01,  2.60971148e-01, 0.0, 0.0, 0.0], p[1.09531298e-02, -6.81968548e-01,  2.60971148e-01, 0.0, 0.0, 0.0], a=0.05,v=0.1,r=0.02,mode=1)"+"\n").encode('utf8'))

        # time.sleep(1)

        # self.con.send((f"movec(p[-0.40468702e-02, -5.51968548e-01,  2.60971148e-01, 0.0, 0.0, 0.0], [1.09531297e-02, -3.81969999e-01,  2.60971148e-01, 0.0, 0.0, 0.0], a=0.05,v=0.1,r=0.02,mode=1)"+"\n").encode('utf8'))

        # self.con.send((f"mc_run_motion(id=-1)\n").encode('utf8'))
        time.sleep(5)

    def disconnect(self):
        self.con.close()