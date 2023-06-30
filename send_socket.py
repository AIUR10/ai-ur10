#!/usr/bin/env python

import time
import socket
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


    def send_circular_action(self, initial_position, shared_variable_stop_capture):

        # Here we setup the position 35cm above the object of interest, which is at 35cm
        # from the initial position of UR10
        first_pose_via = initial_position.copy()
        first_pose_via[1] -= 0.35
        first_pose_via[2] += 0.35

        # We setup the position at the end of the semi-circular movement to be behind the 
        # object of interest
        first_pose_to = initial_position.copy()
        first_pose_to[1] -= 0.7

        # We send the first semi-circular instruction to UR10
        self.con.send((f"movec(p{first_pose_via}, p{first_pose_to}, a=0.01,v=0.1,r=0,mode=1)"+"\n").encode('utf8'))

        # We wait 20 seconds in order to let the UR10 make all the movement
        time.sleep(20)

        # Signal to stop the capture by setting up the shared variable to True
        with shared_variable_stop_capture.get_lock():
            shared_variable_stop_capture.value = True

        # We send the seconf semi-circular instruction to UR10 in order to come back to his intial position
        self.con.send((f"movec(p{first_pose_via}, p{initial_position}, a=0.01,v=0.1,r=0,mode=1)"+"\n").encode('utf8'))

        # We wait 20 seconds in order to let the UR10 make all the movement
        time.sleep(20)

    def disconnect(self):
        try:
            self.con.close()
        except:
            pass
        finally:
            pass