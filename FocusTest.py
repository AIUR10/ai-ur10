#Test to get Robotiq Wrist Camera working in OpenCV
import numpy as np
import cv2
import time

device = 2 #Change to 1 or 2 for multiple cameras
vidcap = cv2.VideoCapture(device)
if not vidcap.isOpened():
    print("Cannot open camera {}".format(device))
    exit()

#Turn off Autofocus
vidcap.set(cv2.CAP_PROP_AUTOFOCUS,0)

# Set camera resolution, default is 640x480, able to get 1280x720 working, max may be 2560x1920 (according to robotiq manual) unable to get working-could be due to it being set as a video device vs photo camera
vidcap.set(cv2.CAP_PROP_FRAME_WIDTH,1280) 
vidcap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

 
flipflop = True

for i in range(250,500,5): #Not sure what max and min range are for the camera focus, I found that a value of 450 works well at a 1 ft range under current conditions

    
    vidcap.set(cv2.CAP_PROP_FOCUS,i) #This sets the focus to a value of i
    #print(vidcap.get(cv2.CAP_PROP_FOCUS)) #Always throws back 68.0, not sure why. More info at https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html
    
    # Capture
    ret, frame = vidcap.read()
    
    #check if empty
    if not ret:
        print("Retrieve frame failed...")
        break

    #Get size
    if flipflop:
        size = frame.shape
        print("Camera Frame Size {}".format(size))
        flipflop = False

    # Display 
    cv2.imshow('frame', frame)
    key = cv2.waitKey(20) & 0xFF
    if key == 27:
        break
    print("The current focus value is: {}".format(i))
    time.sleep(0.125)
          
print("Exiting...")
vidcap.release()
cv2.destroyAllWindows()


#More info on OpenCV flags can be found at: https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html
