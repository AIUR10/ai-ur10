#!/usr/bin/env python

from camera import Camera
import asyncio

def main():
    
    # Setup segmenter
    camera = Camera()
    camera.connect(path_to_save_video='data/video.mp4')

    terminate_flag = False

    # Create an event loop
    loop = asyncio.get_event_loop()

    try:
        # Create and run the read_video_capture task
        video_task = loop.create_task(camera.segment_video(output_segmented_path="data/video_segmented.mp4"))

        # Run the event loop until termination condition is met
        loop.run_until_complete(video_task)

    except:
        pass

    finally:
        
        # Stop the event loop
        loop.stop()

    # Disconnect camera connection
    camera.disconnect()

if __name__ == '__main__':
    main()