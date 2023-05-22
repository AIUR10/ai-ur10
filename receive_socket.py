#!/usr/bin/env python

import argparse
import logging
import rtde.rtde as rtde
import rtde.rtde_config as rtde_config
import time

IP = "192.168.135.128" # VM
IP_ENSTA = "147.250.35.20" # ROBOT ENSTA

# parameters
parser = argparse.ArgumentParser()
parser.add_argument('--host', default='192.168.135.128',help='name of host to connect to (localhost)') # VM
parser.add_argument('--port', type=int, default=30004, help='port number (30002)')
parser.add_argument('--samples', type=int, default=0,help='number of samples to record')
parser.add_argument('--frequency', type=int, default=125, help='the sampling frequency in Herz')
parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
parser.add_argument("--buffered", help="Use buffered receive which doesn't skip data", action="store_true")
parser.add_argument("--binary", help="save the data in binary format", action="store_true")
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.INFO)

conf = rtde_config.ConfigFile("record_configuration.xml")
output_names, output_types = conf.get_recipe('out')

con = rtde.RTDE(args.host, args.port)
con.connect()

# settings
con.get_controller_version()
con.send_output_setup(output_names, output_types, frequency=args.frequency)

con.send_start()

# initialize variables
X = 0
Y = 0
Z = 0
RX = 0
RY = 0
RZ = 0

# main loop
if args.samples > 0:
    keep_running = False
try:
    if args.buffered:
        state = con.receive_buffered(args.binary)
    else:
        state = con.receive(args.binary)
    if state is not None:
        X,Y,Z,RX,RY,RZ = state.actual_TCP_pose
        date_and_time = state.timestamp
        print("TIME: "+str(date_and_time)+"\n TCP: pos ["+str(X)+", "+str(Y)+", "+str(Z)+"] m, \n rotation : ["+str(RX)+", "+str(RY)+", "+str(RZ)+"] rad")
        time.sleep(0.1)

except KeyboardInterrupt:
    exit
except rtde.RTDEException:
    exit

con.send_pause()
con.disconnect()