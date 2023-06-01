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
      
    def __init__(self, ip_address_camera=None, model="facebook/sam-vit-huge", device=0) -> None:
        if ip_address_camera is not None:
            self.host = ip_address_camera
            self.port = 8080
        self.device = "cuda"
        self.generator = pipeline("mask-generation", model=model, device=device)

        logging.basicConfig(level=logging.INFO)

    def connect(self, filepath=None, output_path="data/output.avi") -> None:
        if filepath is None:
            self.con = cv2.VideoCapture(f"rtsp://{self.host}:{self.port}/h264_opus.sdp")
        else:
            self.con = cv2.VideoCapture(f"{filepath}")

        self.frame_width = int(self.con.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.con.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fps = int(self.con.get(cv2.CAP_PROP_FPS))
        self.out = cv2.VideoWriter(output_path,cv2.VideoWriter_fourcc('M','J','P','G'), fps, (self.frame_width, self.frame_height))



    async def read(self, terminate_flag):
        colors = np.random.randint(0, 255, size=(256, 3), dtype=np.uint8)
        
        logging.info("Video segmentation...")
        length = int(self.con.get(cv2.CAP_PROP_FRAME_COUNT))
        for _ in tqdm(range(length)):

            # while self.con.isOpened():
            status, frame = self.con.read()

            # if frame is read correctly status is True
            if not status:
                logging.info("Can't receive frame (stream end?). Exiting ...")
                break
            
            output = self.segment(frame, colors)
            # output = frame

            # Set the desired width and height
            # resized_frame = cv2.resize(output, (self.frame_width//3, self.frame_height//3))  
            # resized_frame = cv2.resize(frame, (self.frame_width//3, self.frame_height//3))  

            # # Display the resized frame
            # cv2.imshow('Resized Frame', resized_frame)

            # cv2.waitKey(1)

            # Check if termination flag is set
            if terminate_flag and not status:
                logging.info("Done...")
                break        

    def segment(self, frame, colors, model_type="vit_h", sam_checkpoint="sam_vit_h_4b8939.pth"):
               
        frame = Image.fromarray(frame.astype('uint8'), 'RGB')
        outputs = self.generator(frame)

        masks = outputs["masks"]
        combined_image = self.show_masks_on_image(frame, masks)

        combined_image = cv2.cvtColor(np.array(combined_image), cv2.COLOR_RGB2BGR)
        self.out.write(combined_image)

        return combined_image

    def disconnect(self):
        self.con.release()
        self.out.release()
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
        
        





