#!/usr/bin/env python

from receive_socket import Receive_socket
from send_socket import Send_socket

def main():
    host = "192.168.168.128" # VM
    host_ENSTA = "147.250.35.20" # ROBOT ENSTA

    # Setup receiver and sender
    receiver = Receive_socket(host)
    sender = Send_socket(host)
    receiver.connect()
    sender.connect()


    # Receive position of robot
    socket = receiver.receive()
    print(socket)


    # Send action to robot
    action = [10, -80, 80, 0, 15, 0]
    sender.send(action)

    # Receive position of robot
    socket = receiver.receive()
    print(socket)

    # Disconnect receiver and sender connection
    receiver.disconnect()
    sender.disconnect()


if __name__ == '__main__':
    main()