import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
from matplotlib import animation
import ffmpeg
import skvideo.io

#vidfps = [(1/(np.average(np.diff(timestampWorld)))),(1/(np.average(np.diff(timestampEye0)))),(1/(np.average(np.diff(timestampEye1))))]
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
        writer = cv2.VideoWriter(videosFilePath+'/'+videoNames[ii]+'_f.mp4', fourcc, vidfps[ii], (int(vidWidth),int(vidHeight)))
        #writer = skvideo.io.FFmpegWriter(videosFilePath+'/'+videoNames[ii]+'_f.mp4',inputdict={
        #'-pix_fmt': 'bgr24',
        #'-crf': '0',
        #'-r' : str(vidfps[ii])},
        #outputdict={
       # '-vcodec': 'h264_nvenc',  #use the h.264 codec
        #'-b:v': '60000k',
        #'-crf': '0',           #set the constant rate factor to 0, which is lossless
        #'-r' : str(vidfps[ii])  
       # }) 
        
        print(vidlength)
        for jj in (vidlength): #Iterates through each frame of video
            success,image = vidcap.read()#reads in frame 
            if success:# If it successfully reads in a frame
                writer.write(image)
            else: # If the frame is not successfully read
                continue # Continue    
        vidcap.release()
        

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
                if jj < int(vidLength/2): #If the frame is in the first third of video
                    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) #Convert image to greyscale
                    grays.append(np.average(gray))
                    if np.average(gray) > maxfirstGray:#If the average brightness is greater than the threshold
                        maxfirstGray = np.average(gray)#That average brightness becomes the threshold
                        firstFlashFrame = jj#Get the frame number of the brightest frame
                if jj > int((vidLength)/2):
                    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) #Convert image to greyscale
                    grays.append(np.average(gray))
                    if np.average(gray) > maxsecondGray:#If the average brightness is greater than the threshold
                        maxsecondGray = np.average(gray)#That average brightness becomes the threshold
                        secondFlashFrame = jj #Get the frame number of the brightest frame
            else:#If the frame is not correctly read
                continue#Continue
        #plt.plot(range(len(grays)),grays)
        print(firstFlashFrame, 'First frame')
        print(secondFlashFrame, 'Second frame')
        startFlashFrame.append(firstFlashFrame)
        endFlashFrame.append(secondFlashFrame)
        
        
    return startFlashFrame, endFlashFrame

#reEncodeVids(videosFilePath,videoNames,vidfps)

#startFlashFrame, endFlashFrame = flashDetection(videosFilePath,videoNames)

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
    #outputCam_views = [outputWorldView, outputRightEye, outputLeftEye]
    for ii in range(len(videoNames)):
        timestamps = []
    
        vidcap = cv2.VideoCapture(videosFilePath+'/'+videoNames[ii]+'_f_c.mp4')#Open video
        vidLength = range(int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)))
        vidfps = vidcap.get(cv2.CAP_PROP_FPS)
        timestamps = [x/vidfps for x in vidLength] 
        timestamps = np.array(timestamps)
        np.savetxt(videosFilePath+'/'+videoNames[ii]+'_timestamps.txt',timestamps)


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
#ginput(videosFilePath, videoNames)

def plotVideosTogether(videosFilePath,videoNames):
    #Open all Video Files
    worldVidCap = cv2.VideoCapture(videosFilePath+'/'+videoNames[0]+'_f_c.mp4')
    eye0VidCap = cv2.VideoCapture(videosFilePath+'/'+videoNames[1]+'_f_c.mp4')
    eye1VidCap = cv2.VideoCapture(videosFilePath+'/'+videoNames[2]+'_f_c.mp4')
    #Get fps of each video
    worldfps = worldVidCap.get(cv2.CAP_PROP_FPS)
    eye0fps = eye0VidCap.get(cv2.CAP_PROP_FPS)
    eye1fps = eye1VidCap.get(cv2.CAP_PROP_FPS)
    #Put Video Lengths and FPS into a list
    vidLengths = [worldVidCap.get(cv2.CAP_PROP_FRAME_COUNT),eye0VidCap.get(cv2.CAP_PROP_FRAME_COUNT),eye1VidCap.get(cv2.CAP_PROP_FRAME_COUNT)]
    vidFPS = [worldfps, eye0fps,eye1fps]
   
    #Read in timestamp files
    world_timestamps = np.load(videosFilePath+'/'+videoNames[0]+'_timestamps.npy')
    eye0_timestamps = np.load(videosFilePath+'/'+videoNames[1]+'_timestamps.npy')
    eye1_timestamps = np.load(videosFilePath+'/'+videoNames[2]+'_timestamps.npy')
    #Create list for syncing the timestamps
    syncEye0 = []
    syncEye1 = []
    syncEye0TS = []
    syncEye1TS = []
    
    for ii in range(len(world_timestamps)):#Iterate through the video with least timestamps(should always be world view)
        if ii == 2800:
            break
        #Find the value in the eye timstamps list that is closest to each value in world timestamps
        syncEye0TS.append(min(eye0_timestamps, key=lambda x:abs(x-world_timestamps[ii])))
        syncEye1TS.append(min(eye1_timestamps, key=lambda y:abs(y-world_timestamps[ii])))
        if ii%1000 ==0:
            print(ii)
    # Multiply by the fps to make a list of the synced frame numbers
    for xx in syncEye0TS:
        syncEye0.append(int(xx*eye0fps))
    for xx in syncEye1TS:
        syncEye1.append(int(xx*eye1fps))
    syncWorld = []
    for xx in world_timestamps:
        syncWorld.append(int(xx*worldfps))
    #Intialize the video writer
    Writer = animation.FFMpegWriter(fps = 10)
    fig = plt.figure(constrained_layout=False)
    #Create a plot with the two eye videos on bottom and world on top
    grid = fig.add_gridspec(2,3)
    ax1 = fig.add_subplot(grid[0,:])
    ax2 = fig.add_subplot(grid[1,0])
    ax3 = fig.add_subplot(grid[1,2])
    startFrame = 2100
    endFrame = 2800
    #Open video writer
    worldFrame = False
    eye0Frame = False
    eye1Frame = False
    with Writer.saving(fig,videosFilePath+'/'+'World+Eyes.mp4',100):
        for jj in range(len(eye1_timestamps)): #iterate through length of eye timestamps
            worldSuccess, worldImage = worldVidCap.read()
            eye0Success, eye0Image = eye0VidCap.read()
            eye1Success, eye1Image = eye1VidCap.read()
            if jj < startFrame: #If the index is before when you want to start 
                continue   
            if jj in syncWorld:
                worldFrame = True              
            if jj in syncEye0:
                eye0Frame = True
            if jj in syncEye1:
                eye1Frame = True        
            print(worldFrame,eye0Frame,eye1Frame,'Frame',jj)  
            if worldFrame ==True and eye1Frame == True and eye0Frame == True:
                #eye0Image = cv2.flip(eye0Image,0)#Flip the eye
                worldImage = cv2.cvtColor(worldImage,cv2.COLOR_BGR2RGB)#Make world rgb
                #Show each image 
                ax1.imshow(worldImage)
                ax2.imshow(eye1Image)
                ax3.imshow(eye0Image)
                #Write the frame to video
                Writer.grab_frame()
                worldFrame = False
                eye0Frame = False
                eye1Frame = False
            if jj == endFrame:
                break
            '''elif jj in syncEye0 and jj in syncEye1 and jj in syncWorld:
             #If the index is in each list of sunced frames
                #Read the frames
                worldSuccess, worldImage = worldVidCap.read()
                eye0Success, eye0Image = eye0VidCap.read()
                eye1Success, eye1Image = eye1VidCap.read()
               
                eye0Image = cv2.flip(eye0Image,0)#Flip the eye
                worldImage = cv2.cvtColor(worldImage,cv2.COLOR_BGR2RGB)#Make world rgb
                #Show each image 
                ax1.imshow(worldImage)
                ax2.imshow(eye1Image)
                ax3.imshow(eye0Image)
                #Write the frame to video
                Writer.grab_frame()
            '''
            
    print('')
#plotVideosTogether(videosFilePath,videoNames)