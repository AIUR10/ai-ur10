#!/usr/bin/env python

import cv2
import logging
from metaseg import SegAutoMaskPredictor

class Camera():
      
    def __init__(self, ip_address_camera=None) -> None:
        if ip_address_camera is not None:
            self.host = ip_address_camera
            self.port = 8080

        logging.basicConfig(level=logging.INFO)


    def connect(self, video_to_segment_path, captureVideo=False) -> None:
        self.captureVideo = captureVideo
        self.video_to_segment_path = video_to_segment_path

        if self.captureVideo:
            self.stream = cv2.VideoCapture(f"rtsp://{self.host}:{self.port}/h264.sdp")
            self.frame_width = int(self.con.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.frame_height = int(self.con.get(cv2.CAP_PROP_FRAME_HEIGHT))

            self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.video_to_segment = cv2.VideoWriter(self.video_to_segment_path, self.fourcc, 50, (self.frame_width//3, self.frame_height//3))


    async def read(self, terminate_flag):
        
        while self.con.isOpened():
            status, frame = self.stream.read()

            # if frame is read correctly status is True
            if not status:
                logging.info("Stream end. Exiting...")
                break

            frame_resized = cv2.resize(frame, (self.frame_width//3, self.frame_height//3))

            self.video_saved.write(frame_resized)

            # Check if termination flag is set
            if terminate_flag and not status:
                logging.info("Done...")
                break 


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
        
        





