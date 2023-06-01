#!/usr/bin/env python

import cv2
import logging
import numpy as np
from segment_anything.modeling import Sam
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry


class Camera():
      
    def __init__(self, ip_address_camera=None) -> None:
        if ip_address_camera is not None:
            self.host = ip_address_camera
            self.port = 8080
        self.device = "cuda"

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

        while self.con.isOpened():
            status, frame = self.con.read()

            # if frame is read correctly status is True
            if not status:
                logging.info("Can't receive frame (stream end?). Exiting ...")
                break

            output = self.segment(frame, colors)
            # output = frame

            # Set the desired width and height
            resized_frame = cv2.resize(output, (self.frame_width//3, self.frame_height//3))  
            # resized_frame = cv2.resize(frame, (self.frame_width//3, self.frame_height//3))  

            # # Display the resized frame
            cv2.imshow('Resized Frame', resized_frame)

            cv2.waitKey(1)

            # Check if termination flag is set
            if terminate_flag:
                break        

    def segment(self, frame, colors, model_type="vit_h", sam_checkpoint="sam_vit_h_4b8939.pth"):
        
        logging.info("Creating sam model...")
        sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
        sam.to(device=self.device)
        logging.info("Done")
        
        
        logging.info("Creating mask generator...")
        mask_generator = SamAutomaticMaskGenerator(sam)
        logging.info("Done")

        logging.info("Generating mask...")
        masks = mask_generator.generate(frame)
        logging.info("Done")

        combined_mask = None

        if len(masks) != 0:

            sorted_anns = sorted(masks, key=(lambda x: x["area"]), reverse=True)
            mask_image = np.zeros(
                (masks[0]["segmentation"].shape[0], masks[0]["segmentation"].shape[1], 3), dtype=np.uint8
            )

            for i, ann in enumerate(sorted_anns):
                m = ann["segmentation"]
                color = colors[i % 256]
                img = np.zeros((m.shape[0], m.shape[1], 3), dtype=np.uint8)
                img[:, :, 0] = color[0]
                img[:, :, 1] = color[1]
                img[:, :, 2] = color[2]
                img = cv2.bitwise_and(img, img, mask=m.astype(np.uint8))
                img = cv2.addWeighted(img, 0.35, np.zeros_like(img), 0.65, 0)
                mask_image = cv2.add(mask_image, img)
            
            combined_mask = cv2.add(frame, mask_image)
            self.out.write(combined_mask)
        
        return combined_mask

    def disconnect(self):
        self.con.release()
        self.out.release()
        cv2.destroyAllWindows()
        





