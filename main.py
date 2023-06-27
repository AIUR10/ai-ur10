#!/usr/bin/env python

from receive_socket import Receive_socket
from send_socket import Send_socket

def main():
    host = "192.168.168.128" # VM
    host_ENSTA = "147.250.35.20" # ROBOT ENSTA

    # Setup receiver and sender
    receiver = Receive_socket(host_ENSTA)
    sender = Send_socket(host_ENSTA)
    receiver.connect()
    sender.connect()


    # Receive position of robot
    socket = receiver.receive()
    print(f"\nSOCKET : {socket}\n")


    # Send action to robot
    action = socket.tolist()
    action[2] += 0.1
    print(f"ACTION : {action}")
    # action = [10, -80, 80, 0, 15, 0]
    sender.send(action)

    # Receive position of robot
    socket = receiver.receive()

    # Disconnect receiver and sender connection
    receiver.disconnect()
    sender.disconnect()


if __name__ == '__main__':
    main()