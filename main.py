#!/usr/bin/env python

from receive_socket import Receive_socket
from send_socket import Send_socket
from camera import Camera
from multiprocessing import Process, Value
import argparse

def observe_object(sender, receiver, shared_variable_stop_capture):

    # Receive position of robot
    current_position = receiver.receive()

    # sender.send(new_position)
    sender.send_circular_action(current_position, shared_variable_stop_capture)

    # Receive position of robot
    current_position = receiver.receive()


def main(host):
    
    # Setup receiver and sender
    receiver = Receive_socket(host)
    sender = Send_socket(host)
    receiver.connect()
    sender.connect()

    # Setup camera
    camera = Camera(device=2) # Change to 1 or 2 for multiple cameras
    camera.connect(video_to_segment_path='data/video.mp4')

    # Creation of shared variable to stop the capture
    shared_variable_stop_capture = Value('b', False)

    # Creating a subprocess which will give action to the UR10
    observe_process = Process(target=observe_object, args=(sender, receiver, shared_variable_stop_capture))
    observe_process.start()

    # The main process capture the object
    camera.read(shared_variable_stop_capture)

    # When the subprocess is finish it join the main process
    observe_process.join()

    # We segment the video captured by the camera
    camera.segment_video(video_segmented_path="data/video_segmented.mp4")
    
    # Disconnect receiver, sender and camera connection
    camera.disconnect()
    receiver.disconnect()
    sender.disconnect()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, help='ip address of the host', required=True)
    args = parser.parse_args()

    main(host=args.host)

