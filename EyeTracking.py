import cv2
import numpy as np
import os

baseFilePath = 'D:/Juggling/JSM/Juggling0003_06142020/EyeTracking'
vidfps = [30,120,120]


worldView = baseFilePath + '/world.mp4'
rightEye = baseFilePath + '/eye0.mp4'
leftEye = baseFilePath + '/eye1.mp4'
cam_views = [worldView, rightEye, leftEye]
outputWorldView = baseFilePath +'/world_f.mp4'
outputRightEye = baseFilePath +'/eye0_f.mp4'
outputLeftEye = baseFilePath +'/eye1_f.mp4'
outputCam_views = [outputWorldView, outputRightEye, outputLeftEye]

video_resolution = cam_views
for ii in range(len(cam_views)):
    vidcap = cv2.VideoCapture(cam_views[ii])#Open video
    vidWidth  = vidcap.get(cv2.CAP_PROP_FRAME_WIDTH) #Get video height
    vidHeight = vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT) #Get video width
    video_resolution = (int(vidWidth),int(vidHeight)) #Create variable for video resolution
    vidfps = vidfps[ii]
    fourcc = cv2.VideoWriter_fourcc(*'H264')
    frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)) #find frame count of video 
    vidlength = range(int(frame_count)) #Create list for loop
    writer = cv2.VideoWriter(outputCam_views[ii], fourcc, 120, (int(vidWidth),int(vidHeight)))
    for jj in (vidlength): #Iterates through each frame of video
        success,image = vidcap.read()#reads in frame 
        if success:# If it successfully reads in a frame
            writer.write(image)
        else: # If the frame is not successfully read
            continue # Continue    
    vidcap.release()
    writer.release()
