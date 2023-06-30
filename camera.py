#!/usr/bin/env python

import cv2
import logging
from metaseg import SegAutoMaskPredictor

class Camera():
      
    def __init__(self, device) -> None:
        self.device = device 
        logging.basicConfig(level=logging.INFO)


    def connect(self, video_to_segment_path) -> None:
        self.video_to_segment_path = video_to_segment_path

        self.stream = cv2.VideoCapture(self.device)
        self.frame_width = int(self.stream.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_to_segment = cv2.VideoWriter(self.video_to_segment_path, self.fourcc, 50, (self.frame_width, self.frame_height))
        
    def read(self, shared_variable_stop_capture):

        while self.stream.isOpened():
            status, frame = self.stream.read()

            # Stop_capture is a shared variable which is setup to True
            # when the first semi-circular movement is done, 
            # see send_circular_action in send_socket.py
            stop_capture = shared_variable_stop_capture.value

            # If frame is read correctly status is True 
            if not status or stop_capture:
                logging.info("Stream end. Exiting...")
                break

            # To observe in real-time the capture
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
        self.stream.release()
        self.video_to_segment.release()
        cv2.destroyAllWindows()
        
        





