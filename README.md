# ai-ur10

Project Title: AI-UR10 Shoe Personalization

# Overview

This project aims to utilize the UR10 robot to personalize shoes by observing the object in space, segmenting it, creating a 3D model, and adding customized tags based on the model. The following steps outline the process to achieve this goal:

# Steps

1. Observing the object in space

The UR10 robot is employed in this step to record a video of the shoe from various perspectives in a 3D environment. For later steps, the video footage will be an essential source of information. Make sure the robot is calibrated correctly and able to move around the object to gather complete visual data.

Here is the joint position for his initial position:
Base:       -90.00°
Shoulder:   -50.00°
Elbow:      -160.00°
Wrist 1:    30.00°
Wrist 2:    90.00°
Wrist 3:    0.00°

We initially intended to move in a circle around the object, but encountered issues such as: 
- Impact issues because the UR10 was touching the object of interest 
- Singularity points that forced the UR10 to move in a way that prevented him from making a second semi-circular movement to return to his starting position.

As a result, we try a different strategy by moving semi-circularly above the robot. This method is easier because the outgoing and return movements are identical. However, we see very tiny variations between outbound and return movement, which, depending on the location of the item of interest, leads to somewhat superior tracking for either the outbound or return travel. In order to ensure that we had enough information to continue with the project's second phase, we decided to only catch the object during its outward motion. 

2. Segment the object

After the video has been recorded, the process of distinguishing the shoe item from the background begins. This segmentation process aims to identify specific shoe parts that can be changed. To precisely isolate the shoe item, use segmentation techniques like "Segment Anything."

So, after filming the subject of interest, we attempt to cut the movie into separate parts using Segment Anything. To do this, we employ the library'metaseg' which already has a function that takes a video as an argument and returns a segmented video. Unfortunately, if your GPU has less than 5GB, we can't use this model. We use a second computer to create the segmentation because we don't have this resource on a single laptop.

In terms of how long it takes to segment the video, we presummated previously that splitting the movie in half affects the segmentation process. In essence, by recording the outward and return movements, we were able to capture a film of about 18 seconds, which took about 18 minutes to segment. By solely recording the outward motion, we were able to get an 8-second video that took 8 minutes to segment.

3. Use 3D modeling (not implemented yet)

The goal is to construct a 3D model of the shoe once the object has been correctly segmented. The 3D model will give a thorough picture of the shoe's physical design and act as a guide for accurate modification. Create the 3D model from the segmented video footage using the relevant software libraries, such as OpenCV or Meshroom.

4. Customizable areas (not implemented yet)

The UR10 robot can be given instructions on where to apply customized tags on the shoe using a marker based on the 3D model created in the previous stage. The exact placements, orientations, and dimensions of the tags will be determined with the help of the 3D model. To ensure precise and consistent customisation, make sure the robot and marker tool are effectively communicating with one another.

# Installation

You need to install IP Webcam (https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en_IN&pli=1) on your smartphone and activate the setting 'This is a public camera' in 'Local broadcasting' settings. Then 'Start server' by clicking on the three dots on top-right of the application.

To use Segment Anything you need to Microsoft Visual C++ greather than 14 version.

Before testing our project, meet all the requirements in requirements.txt

In order to use the Segment Anything, you will need a certain amount of GPU. Minimum requirements: **5 GB**
