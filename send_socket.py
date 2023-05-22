#!/usr/bin/env python
import time
import socket
import math

IP = "192.168.135.128" # VM
IP_ENSTA = "147.250.35.20" # ROBOT ENSTA

# parameters

s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
s.connect ((IP, 30001))

joint_positions_degrees = [0, -128.19, 79.71, -131.52, 0, 0]
joint_positions_radians = [math.radians(jpd) for jpd in joint_positions_degrees]

s.send ((f"movel({joint_positions_radians}, a=1, v=1)"+"\n").encode('utf8'))
time.sleep(1)

s.close ()