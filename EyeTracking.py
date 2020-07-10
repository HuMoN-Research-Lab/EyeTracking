import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
videosFilePath = 'D:/Juggling/JSM/Juggling0003_06142020/EyeTracking'
vidfps = [30,120,120]

def reEncodeVids(videosFilePath,vidfps):
    worldView = videosFilePath + '/world.mp4'
    rightEye = videosFilePath + '/eye0.mp4'
    leftEye = videosFilePath + '/eye1.mp4'
    cam_views = [worldView, rightEye, leftEye]
    outputWorldView = videosFilePath +'/world_f.mp4'
    outputRightEye = videosFilePath +'/eye0_f.mp4'
    outputLeftEye = videosFilePath +'/eye1_f.mp4'
    outputCam_views = [outputWorldView, outputRightEye, outputLeftEye]

    video_resolution = cam_views
    for ii in range(len(cam_views)):
        vidcap = cv2.VideoCapture(cam_views[ii])#Open video
        vidWidth  = vidcap.get(cv2.CAP_PROP_FRAME_WIDTH) #Get video height
        vidHeight = vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT) #Get video width
        video_resolution = (int(vidWidth),int(vidHeight)) #Create variable for video resolution
        
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)) #find frame count of video 
        vidlength = range(int(frame_count)) #Create list for loop
        writer = cv2.VideoWriter(outputCam_views[ii], fourcc, vidfps[ii], (int(vidWidth),int(vidHeight)))
        for jj in (vidlength): #Iterates through each frame of video
            success,image = vidcap.read()#reads in frame 
            if success:# If it successfully reads in a frame
                writer.write(image)
            else: # If the frame is not successfully read
                continue # Continue    
        vidcap.release()
        writer.release()

def flashDetection(videosFilePath):
    worldView = videosFilePath + '/world_f.mp4'
    rightEye = videosFilePath + '/eye0_f.mp4'
    leftEye = videosFilePath + '/eye1_f.mp4'
    cam_views = [worldView, rightEye, leftEye]
    startFlashFrame = []
    endFlashFrame = []
    for ii in range(len(cam_views)):
        vidcap = cv2.VideoCapture(cam_views[ii])#Open video
        vidWidth  = vidcap.get(cv2.CAP_PROP_FRAME_WIDTH) #Get video height
        vidHeight = vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT) #Get video width
        video_resolution = (int(vidWidth),int(vidHeight)) #Create variable for video resolution
        vidLength = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
        vidfps = vidcap.get(cv2.CAP_PROP_FPS)
        success,image = vidcap.read() #read a frame
        maxfirstGray = 0 #Intialize the variable for the threshold of the max brightness of beginning of video
        maxsecondGray = 0 #Intialize the variable for the threshold of the max brightness of end of video
        grays = []
        for jj in range(int(vidLength)):#For each frame in the video
            
            success,image = vidcap.read() #read a frame
            if success: #If frame is correctly read
                if jj < int(vidLength/3): #If the frame is in the first third of video
                    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) #Convert image to greyscale
                    grays.append(np.average(gray))
                    if np.average(gray) > maxfirstGray:#If the average brightness is greater than the threshold
                        maxfirstGray = np.average(gray)#That average brightness becomes the threshold
                        firstFlashFrame = jj#Get the frame number of the brightest frame
                if jj > int((2*vidLength)/3):
                    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) #Convert image to greyscale
                    grays.append(np.average(gray))
                    if np.average(gray) > maxsecondGray:#If the average brightness is greater than the threshold
                        maxsecondGray = np.average(gray)#That average brightness becomes the threshold
                        secondFlashFrame = jj #Get the frame number of the brightest frame
            else:#If the frame is not correctly read
                continue#Continue
        startFlashFrame.append(firstFlashFrame)
        endFlashFrame.append(secondFlashFrame)
        plt.plot(grays)
        plt.title('Brightness of frames')
        plt.xlabel('Frames')
        plt.ylabel('Brightness')
        plt.show()
        
    return startFlashFrame, endFlashFrame

#reEncodeVids(videosFilePath,vidfps)

startFlashFrame, endFlashFrame = flashDetection(videosFilePath)

def trimVids(videosFilePath, startFlashFrame,endFlashFrame):
    worldView = videosFilePath + '/world_f.mp4'
    rightEye = videosFilePath + '/eye0_f.mp4'
    leftEye = videosFilePath + '/eye1_f.mp4'
    cam_views = [worldView, rightEye, leftEye]
    outputWorldView = videosFilePath +'/world_f_c.mp4'
    outputRightEye = videosFilePath +'/eye0_f_c.mp4'
    outputLeftEye = videosFilePath +'/eye1_f_c.mp4'
    outputCam_views = [outputWorldView, outputRightEye, outputLeftEye]
    for ii in range(len(cam_views)):
        input1 = ffmpeg.input(cam_views[ii])#input for ffmpeg

        node1_1 = input1.trim(start_frame=startFlashFrame[ii],end_frame=endFlashFrame[ii]).setpts('PTS-STARTPTS')#Trim video based on the frame numbers
        node1_1.output(outputCam_views[ii]).run()#Save to output folder

trimVids(videosFilePath, startFlashFrame, endFlashFrame)

def saveTimeStamps(videosFilePath): 
    worldView = videosFilePath + '/world_f_c.mp4'
    rightEye = videosFilePath + '/eye0_f_c.mp4'
    leftEye = videosFilePath + '/eye1_f_c.mp4'
    cam_views = [worldView, rightEye, leftEye]
    outputWorldView = videosFilePath +'/world_timestamps.txt'
    outputRightEye = videosFilePath +'/eye0_timestamps.txt'
    outputLeftEye = videosFilePath +'/eye1_timestamps.txt'
    outputCam_views = [outputWorldView, outputRightEye, outputLeftEye]
    for ii in len(range(cam_views)):
        timestamps = []
        vidcap = cv2.VideoCapture(cam_views[ii])#Open video
        vidLength = range(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
        vidfps = vidcap.get(cv2.CAP_PROP_FPS)
        timestamps = vidlength/vidfps
        timestamps = np.array(timestamps)
        np.savetxt(outputCam_views)


saveTimeStamps(videosFilePath)


def ginput(videosFilePath):
    for ii in range(len(cam_views)):
        vidcap = cv2.VideoCapture(cam_views[ii])#Open video
        vidWidth  = vidcap.get(cv2.CAP_PROP_FRAME_WIDTH) #Get video height
        vidHeight = vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT) #Get video width
        video_resolution = (int(vidWidth),int(vidHeight)) #Create variable for video resolution
        vidfps = vidfps[ii]
        frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)) #find frame count of video 
        vidlength = range(int(frame_count)) #Create list for loop
        for jj in (vidlength): #Iterates through each frame of video
            success,image = vidcap.read()#reads in frame 
            if success:# If it successfully reads in a frame
                cv2.imshow(image)
                x = plt.ginput(4)
                print(x)
            else: # If the frame is not successfully read
                continue # Continue    
        vidcap.release()
        