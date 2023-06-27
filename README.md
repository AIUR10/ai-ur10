# ai-ur10

Project Title: AI-UR10 Shoe Personalization

# Overview

This project aims to utilize the UR10 robot to personalize shoes by observing the object in space, segmenting it, creating a 3D model, and adding customized tags based on the model. The following steps outline the process to achieve this goal:

# Steps

1. Observing the object in space

The UR10 robot is employed in this step to record a video of the shoe from various perspectives in a 3D environment. For later steps, the video footage will be an essential source of information. Make sure the robot is calibrated correctly and able to move around the object to gather complete visual data.

2. Segment the object

The process of separating the shoe object from the background comes after the video has been captured. This segmentation procedure seeks to pinpoint particular shoe components that can be altered. Use segmentation methods to precisely isolate the shoe item, such as "Segment Anything."

3. Use 3D modeling (not implemented yet)

The goal is to construct a 3D model of the shoe once the object has been correctly segmented. The 3D model will give a thorough picture of the shoe's physical design and act as a guide for accurate modification. Create the 3D model from the segmented video footage using the relevant software libraries, such as OpenCV or Meshroom.

4. Customizable areas (not implemented yet)

The UR10 robot can be given instructions on where to apply customized tags on the shoe using a marker based on the 3D model created in the previous stage. The exact placements, orientations, and dimensions of the tags will be determined with the help of the 3D model. To ensure precise and consistent customisation, make sure the robot and marker tool are effectively communicating with one another.

# Installation

You need to install IP Webcam (https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en_IN&pli=1) on your smartphone and activate the setting 'This is a public camera' in 'Local broadcasting' settings. Then 'Start server' by clicking on the three dots on top-right of the application.

To use Segment Anything you need to Microsoft Visual C++ greather than 14 version.

Before testing our project, meet all the requirements in requirements.txt

In order to use the Segment Anything, you will need a certain amount of GPU. Minimum requirements: **6 GB**
