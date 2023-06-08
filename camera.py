#!/usr/bin/env python

import cv2
import logging
import numpy as np
from transformers import pipeline
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
import gc
from tqdm import tqdm


class Camera():
      
    def __init__(self, ip_address_camera=None, model="facebook/sam-vit-base", device=0) -> None:
        if ip_address_camera is not None:
            self.host = ip_address_camera
            self.port = 8080
        self.device = "cuda"
        self.generator = pipeline("mask-generation", model=model, device=device)

        logging.basicConfig(level=logging.INFO)


    def connect(self, path_to_save_video, captureVideo=False) -> None:
        self.captureVideo = captureVideo
        self.path_to_save_video = path_to_save_video
        self.video_segmented = None

        if self.captureVideo:
            self.con = cv2.VideoCapture(f"rtsp://{self.host}:{self.port}/h264.sdp")
            self.frame_width = int(self.con.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.frame_height = int(self.con.get(cv2.CAP_PROP_FRAME_HEIGHT))

            self.fps = int(self.con.get(cv2.CAP_PROP_FPS))
            self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.video_saved = cv2.VideoWriter(self.path_to_save_video, self.fourcc, self.fps, (self.frame_width, self.frame_height))
        else:
            self.video_to_segment = cv2.VideoCapture(f"{self.path_to_save_video}")
            self.frame_width = int(self.video_to_segment.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.frame_height = int(self.video_to_segment.get(cv2.CAP_PROP_FRAME_HEIGHT))

            self.fps = int(self.video_to_segment.get(cv2.CAP_PROP_FPS))

    async def read(self, terminate_flag):
        
        while self.con.isOpened():
            status, frame = self.con.read()

            # if frame is read correctly status is True
            if not status:
                logging.info("Can't receive frame (stream end?). Exiting ...")
                break
            
            self.video_saved.write(frame)

            cv2.imshow("frame",frame)
            cv2.waitKey(1)

            # Check if termination flag is set
            if terminate_flag and not status:
                logging.info("Done...")
                break 


    def segment_video(self, output_segmented_path):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_segmented = cv2.VideoWriter(output_segmented_path, fourcc, self.fps, (self.frame_width, self.frame_height))

        colors = np.random.randint(0, 255, size=(256, 3), dtype=np.uint8)
            
        logging.info("Video segmentation...")
        length = int(self.video_to_segment.get(cv2.CAP_PROP_FRAME_COUNT))

        for _ in tqdm(range(length)):

            status, frame = self.video_to_segment.read()

            # if frame is read correctly status is True
            if not status:
                logging.info("Can't receive frame (stream end?). Exiting ...")
                break
            
            segmented_image = self.segment(frame, colors)

            self.video_segmented.write(segmented_image)
        
        logging.info("Done")              

    def segment(self, frame):
               
        frame = Image.fromarray(frame.astype('uint8'), 'RGB')
        outputs = self.generator(frame)

        masks = outputs["masks"]
        segmented_image = self.show_masks_on_image(frame, masks)

        segmented_image = cv2.cvtColor(np.array(segmented_image), cv2.COLOR_RGB2BGR)
        
        return segmented_image


    def disconnect(self):
        if self.captureVideo:
            self.con.release()
            self.video_saved.release()
        else:
            self.video_to_segment.release()
            self.video_segmented.release()
        cv2.destroyAllWindows()
        

    def show_masks_on_image(self, raw_image, masks):
        combined_image = Image.fromarray(np.array(raw_image))

        for mask in masks:
            color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
            h, w = mask.shape[-2:]
            mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
            mask_image = Image.fromarray((mask_image * 255).astype(np.uint8))
            combined_image.paste(mask_image, (0, 0), mask_image)

        return combined_image
        
        





