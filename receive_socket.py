#!/usr/bin/env python

import logging
import sys
sys.path.append('./docs')
import rtde.rtde as rtde
import rtde.rtde_config as rtde_config
import time

class Receive_socket():

    def __init__(self, ip_address) -> None:
        self.host = ip_address
        self.port = 30004
        self.frequency = 125

        logging.basicConfig(level=logging.INFO)

        conf = rtde_config.ConfigFile("lib/record_configuration.xml")
        self.output_names, self.output_types = conf.get_recipe('out')

    def connect(self) -> None:
        self.con = rtde.RTDE(self.host, self.port)
        self.con.connect()

        # Settings
        self.con.get_controller_version()
        self.con.send_output_setup(self.output_names, self.output_types, frequency=self.frequency)

        self.con.send_start()

    def receive(self):

        # initialize variables
        X, Y, Z, RX, RY, RZ = 0, 0, 0, 0, 0, 0

        try:
            state = self.con.receive()
            if state is not None:
                X, Y, Z, RX, RY, RZ = state.actual_TCP_pose
                logging.info(f"Current position: [{X}, {Y}, {Z}, {RX}, {RY}, {RZ}]")
                time.sleep(0.1)

        except KeyboardInterrupt:
            exit
        except rtde.RTDEException:
            exit

        current_position = eval(f"[{X}, {Y}, {Z}, {RX}, {RY}, {RZ}]")

        return current_position

    def disconnect(self) -> None: 
        try:
            self.con.send_pause()
            self.con.disconnect()
        except:
            pass
        finally:
            pass