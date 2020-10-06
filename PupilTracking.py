import numpy as np
import cv2 
import pandas as pd
import math
from skimage import morphology, measure
import scipy
from matplotlib import pyplot as plt
from matplotlib import animation
import skvideo.io

#User input path and video name variables
#basePath = 'D:/Juggling/JSM/Juggling0003_06142020/EyeTracking'
#worldVideoName = 'world'
#eye1VideoName = 'eye0_f_c'
#eye2VideoName = 'eye1'

def PupilTrack(basePath,videoNames):
    
    for ii in range(len(videoNames)):
        
        vidcap = cv2.VideoCapture(basePath+'/'+videoNames[ii]+'_f_c.mp4')#Open video
        vidfps = vidcap.get(cv2.CAP_PROP_FPS)
        vidWidth  = vidcap.get(cv2.CAP_PROP_FRAME_WIDTH) #Get video height
        vidHeight = vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT) #Get video width
        video_resolution = (int(vidWidth),int(vidHeight)) #Create variable for video resolution
        frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)) #find frame count of video
        vidlength = range(frame_count)
        #outputVid = cv2.VideoWriter(basePath + '/' + videoNames[ii]+'_pupilTrack.mp4',-1,30,(int(vidWidth),int(vidHeight)))
        #Open up a video writer variable 
        Writer = animation.FFMpegWriter(fps = 30)

        #Create array for eye positions
        porXY = np.zeros((frame_count,2))
        #Find center of video resolution
        diagPx = np.sqrt(int(vidWidth)^2 + int(vidHeight)^2)

        #Create the plot axis

        fig = plt.figure(constrained_layout=False)
        grid = fig.add_gridspec(3,3)
        ax1 = fig.add_subplot(grid[0,:])
        ax2 = fig.add_subplot(grid[1,0])
        ax3 = fig.add_subplot(grid[1,1])
        ax4 = fig.add_subplot(grid[1,2])
        ax5 = fig.add_subplot(grid[2,:])
        #Open the writer
        with Writer.saving(fig,basePath+'/'+videoNames[ii]+'pupilTrack.mp4',100):
            for jj in vidlength:#For every frame
                success,image = vidcap.read()#reads in frame 
                if success:# If it successfully reads in a frame
                    
                    imgGrey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #Convert image to grey
                    imgGrey = 255 - imgGrey #Subtract by max color number
                    imBin = imgGrey #Create imBin varibale the same size of imgGrey 
                    for rr in range(len(imgGrey)): #for every pixels in the image
                        imBin[rr] = imgGrey[rr] >210 #If the pixel is greater than 200 put it in the imBin varibale as true
                    imBin = imBin*255 #Multiply the bool value by 255 
                    imBlur = cv2.blur(imBin, (4,4)) #Blur the image
                    ret, imCB = cv2.threshold(imBin, 127, 255, 0)#Threshold the image 
                    cv2.imshow('i',imCB)
                    cv2.waitKey(5000)
                    #Find all of the ellipses in the frame
                    label_img  = measure.label(imCB)
                    if np.max(label_img) ==0:
                        continue
                    else:
                        props = measure.regionprops_table(label_img, properties=('centroid',
                                                            'orientation',
                                                            'major_axis_length',
                                                            'minor_axis_length'))
                        biggestBlob = 0 #intialize the biggestBlob as zero
                        props = pd.DataFrame(props) #Make the props array an dataframe
                        MA = (props[["major_axis_length"]]) #Take all the major axis lengths of the blobs detected
                        biggestBlobIndex = 0 #Initilize the biggest blob index
                        for x in range(len(MA)): #For every blob detected
                            if MA.loc[x].values > biggestBlob: #If the major axis is bigger than the biggest one currently detected
                                biggestBlob = MA.loc[x].values #That major axis becomes the biggest blob
                                biggestBlobIndex = x #Take the index of the biggest blob
                        #Take features of the elipse throught the biggest index range 
                        majorAxisLength = float(MA.loc[biggestBlobIndex].values) 
                        minorAxisLength = float(props[["minor_axis_length"]].loc[biggestBlobIndex].values)
                        centroidY = int(props[["centroid-0"]].loc[biggestBlobIndex].values)
                        centroidX = int(props[["centroid-1"]].loc[biggestBlobIndex].values)
                        centroid = [centroidX, centroidY]
                        orientation = float(props[["orientation"]].loc[biggestBlobIndex].values)
                        oriAngle = np.rad2deg(orientation)  #switch orientation to degree

                        porXY[jj,:] = centroid #Store the centroid
                        
                        majorAxisRadius = int(majorAxisLength/2)
                        minorAxisRadius = int(minorAxisLength/2)
                        #Create an ellipse over the pupil in the image
                        cv2.ellipse(image,((centroidX,centroidY)),(majorAxisRadius,minorAxisRadius),oriAngle,0,360,(0,0,255),3)
                        cv2.imshow('',image)
                        cv2.waitKey(300)
                        porWindow = int(vidfps)*5 #Create window for plotting
                        
                        #All this is indexing for plotting
                        if jj >porWindow:
                            step = 1
                        else:
                            step = -1
                        maxIndex = []
                        minIndex = []  
                        if jj -porWindow ==1:
                            maxIndex = 1
                        else:
                            for y in (range(1, (jj-porWindow), step)):
                                maxIndex.append(y)
                            maxIndex  = np.max(maxIndex)
                        if jj+porWindow < len(porXY):
                            step = -1
                        else:
                            step = 1
                        if len(porXY) == (jj+porWindow):
                            minindex = len(porXY)
                        else:
                            for x in (range(len(porXY), (jj+porWindow), step)):
                                minIndex.append(x)
                            minIndex = np.min(minIndex)
                    
                        if jj == vidlength[-1]:
                            continue
                        else:
                            ax1.cla()
                            ax2.cla()
                            ax3.cla()
                            ax4.cla()
                            ax5.cla()                
                            ax1.imshow(image)
                            ax2.imshow(imBin)
                            ax3.imshow(imBlur)
                            ax4.imshow(imCB)

                            ax5.plot(porXY[maxIndex:minIndex,:])
                            
                            im = plt.gcf()
                            Writer.grab_frame()
                if jj%100 ==0:
                    print(jj)
            #ani = animation.ArtistAnimation(fig,ims,interval= 8.3,blit = True)
            
            np.save(basePath+'/'+videoNames[ii]+'_pupilTrack.npy', porXY)         
    return(porXY)
