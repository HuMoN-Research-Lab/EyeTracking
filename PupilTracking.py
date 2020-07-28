import numpy as np
import cv2 
import pandas as pd
import math
from skimage import morphology, measure
import scipy
from matplotlib import pyplot as plt
from matplotlib import animation
import skvideo.io

basePath = 'C:/Users/chris/EyeTracking/Data'
sessionID = '2020-07-20_000_Juggling'


worldVideoName = 'world'
eye1VideoName = 'eye0'
eye2VideoName = 'eye1'
videoNames  = [worldVideoName, eye1VideoName, eye2VideoName]
#for ii in range(len(videoNames)):
vidcap = cv2.VideoCapture(basePath+'/'+videoNames[1]+'_f.mp4')#Open video
vidfps = vidcap.get(cv2.CAP_PROP_FPS)
vidWidth  = vidcap.get(cv2.CAP_PROP_FRAME_WIDTH) #Get video height
vidHeight = vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT) #Get video width
video_resolution = (int(vidWidth),int(vidHeight)) #Create variable for video resolution
'''writer = animation.FFmpegWriter(basePath+'/'+videoNames[1]+'_f_pupilTrack.mp4',inputdict={
    '-pix_fmt': 'bgr24',
    #'-crf': '0',
    '-r' : str(vidfps)},
    outputdict={
    '-vcodec': 'h264_nvenc',  #use the h.264 codec
    '-b:v': '60000k',
    '-crf': '1',           #set the constant rate factor to 0, which is lossless
    '-r' : str(vidfps)  
    }) '''
Writer = animation.FFMpegWriter(fps = 30)


frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)) #find frame count of video 
porXY = np.zeros((frame_count,2))
vidlength = range(frame_count)
diagPx = np.sqrt(int(vidWidth)^2 + int(vidHeight)^2)
fig = plt.figure(constrained_layout=False)
grid = fig.add_gridspec(3,3)
ax1 = fig.add_subplot(grid[0,:])
ax2 = fig.add_subplot(grid[1,0])
ax3 = fig.add_subplot(grid[1,1])
ax4 = fig.add_subplot(grid[1,2])
ax5 = fig.add_subplot(grid[2,:])
with Writer.saving(fig,basePath+'/'+videoNames[1]+'_f_pupilTrack.mp4',100):
    for jj in vidlength:
    
        success,image = vidcap.read()#reads in frame 
        if success:# If it successfully reads in a frame
            #print('frame #', jj, ' of ', frame_count)
            imgGrey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            #ret, thresh = cv2.threshold(imgGrey, 0, 255, cv2.THRESH_BINARY_INV +cv2.THRESH_OTSU)
            imgGrey = 255 - imgGrey
            imBin = imgGrey
            for rr in range(len(imgGrey)):
                imBin[rr] = imgGrey[rr] >200
            imBin = imBin*255
            imBlur = cv2.blur(imBin, (4,4))
            ret, imCB = cv2.threshold(imBin, 127, 255, 0)
            #M = cv2.moments(imCB)
            #cX = int(M["m10"] / M["m00"])
            #cY = int(M["m01"] / M["m00"])
            
            cnts = cv2.findContours(imCB, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]    
            
            if len(cnts) != 0:
                #find the biggest area of the contour
                c = max(cnts, key = cv2.contourArea)
                #rect = cv2.boundingRect(c)
                #(x,y)(MA,ma),angle = cv2.fitEllipse(c)
                label_img  = measure.label(imCB)
                props = measure.regionprops_table(label_img, properties=('centroid',
                                                    'orientation',
                                                    'major_axis_length',
                                                    'minor_axis_length'))
                biggestBlob = 0
                props = pd.DataFrame(props)
                MA = (props[["major_axis_length"]])
                biggestBlobIndex = 0
                for x in range(len(MA)):
                    
                    if MA.loc[x].values > biggestBlob:
                        biggestBlob = MA.loc[x].values
                        biggestBlobIndex = x
                majorAxisLength = float(MA.loc[biggestBlobIndex].values)
                minorAxisLength = float(props[["minor_axis_length"]].loc[biggestBlobIndex].values)
                centroidY = int(props[["centroid-0"]].loc[biggestBlobIndex].values)
                centroidX = int(props[["centroid-1"]].loc[biggestBlobIndex].values)
                centroid = [centroidX, centroidY]
                
                porXY[jj,:] = centroid
                orientation = float(props[["orientation"]].loc[biggestBlobIndex].values)
                oriAngle = np.rad2deg(orientation)
                
                
                twoPi = 2*math.pi
                theta = np.linspace(0,twoPi,100)
                theta = theta.reshape(1,100)
                col = theta
                row = theta
                col = (majorAxisLength/2)*(np.cos(theta))
                col = col.reshape(1,100)
                row = (minorAxisLength/2)*(np.sin(theta))
                row = row.reshape(1,100)

                Transform = np.array([[np.sin(orientation), np.cos(orientation),0,centroidX],[np.cos(-orientation),np.sin(-orientation),0,centroidY],[0,0,1,0],[0,0,0,1]])
                
                zero = np.zeros(100)
                zero = zero.reshape(1,100)
                one = np.ones(100)
                one = one.reshape(1,100)
                D = np.concatenate((col , row , zero, one),axis = 0)          
                D = np.transpose(np.matmul(Transform,D))
                
                center, radius = cv2.minEnclosingCircle(c)
                majorAxisRadius = int(majorAxisLength/2)
                minorAxisRadius = int(minorAxisLength/2)
                cv2.ellipse(image,((centroidX,centroidY)),(majorAxisRadius,minorAxisRadius),oriAngle,0,360,(0,0,255),3)
                


                frames = range(100)
                porWindow = int(vidfps)*5
                #print(porWindow)
                if jj >porWindow:
                    step = 1
                else:
                    step = -1
                maxIndex = []
                minIndex = []  ##############################ADD A continue when jj = porWindow

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
            #eyePos = porXY[[(np.max(maxIndex)):(np.min(minIndex))], :] 
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
                
                
                Writer.grab_frame()
        if jj%1000 ==0:
            print(jj)
            
np.save(basePath+'/'+videoNames[1]+'_f_pupilTrack.npy', porXY)         

            


            
        