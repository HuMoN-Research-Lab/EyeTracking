import cv2
import numpy as np
import os
from matplotlib import pyplot as plt

import ffmpeg
import skvideo.io
videosFilePath = 'D:/Juggling/JSM/Juggling0003_06142020/EyeTracking'
vidfps = [25,90,90]
worldVideoName = 'world'
eye1VideoName = 'eye0'
eye2VideoName = 'eye1'
videoNames  = [worldVideoName, eye1VideoName, eye2VideoName]
def reEncodeVids(videosFilePath,videoNames, vidfps):
    #video_resolution = cam_views
    for ii in range(len(videoNames)):
        vidcap = cv2.VideoCapture(videosFilePath+'/'+videoNames[ii]+'.mp4')#Open video
        vidWidth  = vidcap.get(cv2.CAP_PROP_FRAME_WIDTH) #Get video height
        vidHeight = vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT) #Get video width
        video_resolution = (int(vidWidth),int(vidHeight)) #Create variable for video resolution
        
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)) #find frame count of video 
        vidlength = range(int(frame_count)) #Create list for loop
        #writer = cv2.VideoWriter(videosFilePath+'/'+videoNames[ii]+'_f.mp4', fourcc, vidfps[ii], (int(vidWidth),int(vidHeight)))
        writer = skvideo.io.FFmpegWriter(videosFilePath+'/'+videoNames[ii]+'_f.mp4',inputdict={ '-r' : str(vidfps[ii])  },  outputdict={
        #'-pix_fmt': 'bgr24',
        '-vcodec': 'h264_nvenc',  #use the h.264 codec
        '-crf': '0',           #set the constant rate factor to 0, which is lossless
        '-r' : str(vidfps[ii])  
           #the slower the better compression, in princple, try 
                         #other options see https://trac.ffmpeg.org/wiki/Encode/H.264
        }) 
        
        print(vidlength)
        for jj in (vidlength): #Iterates through each frame of video
            success,image = vidcap.read()#reads in frame 
            if success:# If it successfully reads in a frame
                writer.writeFrame(image)
            else: # If the frame is not successfully read
                continue # Continue    
        vidcap.release()
        writer.close()

def flashDetection(videosFilePath,videoNames):
    '''
    worldView = videosFilePath + '/world_f.mp4'
    rightEye = videosFilePath + '/eye0_f.mp4'
    leftEye = videosFilePath + '/eye1_f.mp4'
    cam_views = [worldView, rightEye, leftEye]'''
    startFlashFrame = []
    endFlashFrame = []
    for ii in range(len(videoNames)):
        vidcap = cv2.VideoCapture(videosFilePath+'/'+videoNames[ii]+'_f.mp4')#Open video
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
        print(firstFlashFrame, 'First frame')
        print(secondFlashFrame, 'Second frame')
        startFlashFrame.append(firstFlashFrame)
        endFlashFrame.append(secondFlashFrame)
        
        
    return startFlashFrame, endFlashFrame

reEncodeVids(videosFilePath,videoNames,vidfps)

startFlashFrame, endFlashFrame = flashDetection(videosFilePath,videoNames)

def trimVids(videosFilePath,videoNames, startFlashFrame,endFlashFrame):
    '''
    worldView = videosFilePath + '/world_f.mp4'
    rightEye = videosFilePath + '/eye0_f.mp4'
    leftEye = videosFilePath + '/eye1_f.mp4'
    cam_views = [worldView, rightEye, leftEye]
    outputWorldView = videosFilePath +'/world_f_c.mp4'
    outputRightEye = videosFilePath +'/eye0_f_c.mp4'
    outputLeftEye = videosFilePath +'/eye1_f_c.mp4'
    
    outputCam_views = [outputWorldView, outputRightEye, outputLeftEye]
    '''
    for ii in range(len(videoNames)):
        input1 = ffmpeg.input(videosFilePath+'/'+videoNames[ii]+'_f.mp4')#input for ffmpeg

        node1_1 = input1.trim(start_frame=startFlashFrame[ii],end_frame=endFlashFrame[ii]).setpts('PTS-STARTPTS')#Trim video based on the frame numbers
        node1_1.output(videosFilePath+'/'+videoNames[ii]+'_f_c.mp4').run()#Save to output folder

#trimVids(videosFilePath,videoNames, startFlashFrame, endFlashFrame)

def saveTimeStamps(videosFilePath,videoNames): 
    '''
    worldView = videosFilePath + '/world_f_c.mp4'
    rightEye = videosFilePath + '/eye0_f_c.mp4'
    leftEye = videosFilePath + '/eye1_f_c.mp4'
    cam_views = [worldView, rightEye, leftEye]
    outputWorldView = videosFilePath +'/world_timestamps.txt'
    outputRightEye = videosFilePath +'/eye0_timestamps.txt'
    outputLeftEye = videosFilePath +'/eye1_timestamps.txt'
    '''
    outputCam_views = [outputWorldView, outputRightEye, outputLeftEye]
    for ii in range(len(videoNames)):
        timestamps = []
        vidcap = cv2.VideoCapture(videosFilePath+'/'+videoNames[ii]+'_f_c.mp4')#Open video
        vidLength = range(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
        vidfps = vidcap.get(cv2.CAP_PROP_FPS)
        timestamps = vidlength/vidfps
        timestamps = np.array(timestamps)
        np.savetxt(videosFilePath+'/'+videoNames[ii]+'_timestamps.txt')


#saveTimeStamps(videosFilePath,videoNames)


def ginput(videosFilePath,videoNames):
    
    for ii in range(len(videoNames)):
        vidcap = cv2.VideoCapture(videosFilePath+'/'+videoNames[ii]+'_f_c.mp4')#Open video
        vidWidth  = vidcap.get(cv2.CAP_PROP_FRAME_WIDTH) #Get video height
        vidHeight = vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT) #Get video width
        video_resolution = (int(vidWidth),int(vidHeight)) #Create variable for video resolution
        #vidfps = vidfps[ii]
        frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)) #find frame count of video 
        vidlength = range(int(frame_count)) #Create list for loop
        for jj in (vidlength): #Iterates through each frame of video
            success,image = vidcap.read()#reads in frame 
            if success:# If it successfully reads in a frame
                plt.imshow(image)
                x = plt.ginput(4)
                print(x)
            else: # If the frame is not successfully read
                continue # Continue    
        vidcap.release()
ginput(videosFilePath, videoNames)
        