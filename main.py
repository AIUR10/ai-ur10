#!/usr/bin/env python

from receive_socket import Receive_socket
from send_socket import Send_socket
from camera import Camera
from multiprocessing import Process, Value


def observe_object(sender, receiver, shared_variable):

    # Receive position of robot
    current_position = receiver.receive()

    # sender.send(new_position)
    sender.send_circular_action(current_position, receiver, shared_variable)

    # Receive position of robot
    current_position = receiver.receive()


def main():
    host = "192.168.168.128" # VM
    host_ENSTA = "147.250.35.20" # ROBOT ENSTA

    # Setup receiver and sender
    receiver = Receive_socket(host_ENSTA)
    sender = Send_socket(host_ENSTA)
    receiver.connect()
    sender.connect()

    camera = Camera()
    camera.connect(video_to_segment_path='data/video.mp4', captureVideo=True)

    shared_variable = Value('b', False)


    observe_process = Process(target=observe_object, args=(sender, receiver, shared_variable))
    observe_process.start()

    camera.read(shared_variable)

    observe_process.join()
    
    # Disconnect receiver, sender and camera connection
    camera.disconnect()
    receiver.disconnect()
    sender.disconnect()


if __name__ == '__main__':
    main()