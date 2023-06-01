#!/usr/bin/env python

from camera import Camera
import asyncio

def main():
    
    # Setup segmenter
    camera = Camera()
    camera.connect('data/PXL_20230601_083011266.ACTIVE.mp4')

    terminate_flag = False

    # Create an event loop
    loop = asyncio.get_event_loop()

    try:
        # Create and run the read_video_capture task
        video_task = loop.create_task(camera.read(terminate_flag))

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