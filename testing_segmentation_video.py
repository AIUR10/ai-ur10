#!/usr/bin/env python

from camera import Camera

def main():
    
    # Setup segmenter
    camera = Camera()
    camera.connect(video_to_segment_path='data/video.mp4')

    camera.segment_video(video_segmented_path="data/video_segmented.mp4")

    # Disconnect camera connection
    camera.disconnect()

if __name__ == '__main__':
    main()