#!/usr/bin/env python

from receive_socket import Receive_socket
from send_socket import Send_socket
import logging


def main():
    host = "192.168.168.128" # VM
    host_ENSTA = "147.250.35.20" # ROBOT ENSTA

    # Setup receiver and sender
    receiver = Receive_socket(host)
    sender = Send_socket(host)
    receiver.connect()
    sender.connect()


    # Receive position of robot
    current_position = receiver.receive()

    # Send action to robot
    new_position = current_position
    new_position[2] = new_position[2] + 0.04
    logging.info(f"Go to: {new_position}")

    sender.send(new_position)

    # Receive position of robot
    current_position = receiver.receive()

    # Disconnect receiver and sender connection
    receiver.disconnect()
    sender.disconnect()


if __name__ == '__main__':
    main()