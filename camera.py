#!/usr/bin/env python

import cv2
import logging
from metaseg import SegAutoMaskPredictor
from receive_socket import Receive_socket
from send_socket import Send_socket

class Camera():
      
    def __init__(self, ip_address_camera=None) -> None:
        if ip_address_camera is not None:
            self.host = ip_address_camera
            self.port = 8080

        logging.basicConfig(level=logging.INFO)


    def connect(self, video_to_segment_path, captureVideo=False) -> None:
        self.captureVideo = captureVideo
        self.video_to_segment_path = video_to_segment_path

        self.terminate_capture = False

        if self.captureVideo:
            # self.stream = cv2.VideoCapture(f"rtsp://{self.host}:{self.port}/h264.sdp")
            device = 2 # Change to 1 or 2 for multiple cameras
            self.stream = cv2.VideoCapture(device)
            self.frame_width = int(self.stream.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.frame_height = int(self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))

            self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.video_to_segment = cv2.VideoWriter(self.video_to_segment_path, self.fourcc, 50, (self.frame_width, self.frame_height))
        
    def read(self, shared_variable):

        
        while self.stream.isOpened():
            status, frame = self.stream.read()

            value = shared_variable.value

            # if frame is read correctly status is True
            if not status or value:
                logging.info("Stream end. Exiting...")
                break

            cv2.imshow('frame', frame)
            cv2.waitKey(20)

            self.video_to_segment.write(frame)
        


    def segment_video(self, video_segmented_path):

        logging.info("Segmenting video...")

        SegAutoMaskPredictor().video_predict(
            source=self.video_to_segment_path,
            model_type="vit_b",
            points_per_side=16, 
            points_per_batch=64,
            min_area=1000,
            output_path=video_segmented_path,
        )
        
        logging.info("Done...")              

    def disconnect(self):
        if self.captureVideo:
            self.stream.release()
            self.video_to_segment.release()
        cv2.destroyAllWindows()
        
        





