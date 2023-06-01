#!/usr/bin/env python

import cv2
import logging

class Camera():
      
    def __init__(self, ip_address_camera=None) -> None:
        if ip_address_camera is not None:
            self.host = ip_address_camera
            self.port = 8080

        logging.basicConfig(level=logging.INFO)

    def connect(self, filepath=None) -> None:
        if filepath is None:
            self.con = cv2.VideoCapture(f"rtsp://{self.host}:{self.port}/h264_opus.sdp")
        else:
            self.con = cv2.VideoCapture(f"{filepath}")

    async def read(self, terminate_flag):

        while self.con.isOpened():
            status, frame = self.con.read()

            # if frame is read correctly status is True
            if not status:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            
            height, width, _ = frame.shape
            resized_frame = cv2.resize(frame, (width//3, height//3))  # Set the desired width and height

            # Display the resized frame
            cv2.imshow('Resized Frame', resized_frame)

            cv2.waitKey(1)

            # Check if termination flag is set
            if terminate_flag:
                break


    def disconnect(self):
        self.con.release()
        cv2.destroyAllWindows()
        





