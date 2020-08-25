import numpy as np
import cv2
from matplotlib import pyplot as  plt

#Filepaths to the videos
worldVidPath = 'D:/Juggling/JSM/Juggling0003_06142020/EyeTracking/world_f_c.mp4'
eye0VidPath =  'D:/Juggling/JSM/Juggling0003_06142020/EyeTracking/eye0_f_c.mp4'
eye1VidPath =  'D:/Juggling/JSM/Juggling0003_06142020/EyeTracking/eye1_f_c.mp4'


#Enter start and end frame
startFrame = 2100
endFrame = 2600

def scatteredInterpolantCalibration(worldVidPath,eye0vidPath,eye1VidPath,startFrame,endFrame):
    kernelOpen=np.ones((5,5))
    kernelClose=np.ones((20,20))
        

    #Open a vidcap for each video
    worldVidCap = cv2.VideoCapture(worldVidPath)
    eye0VidCap = cv2.VideoCapture(eye0VidPath)
    eye1VidCap = cv2.VideoCapture(eye1VidPath)

    #Get frame count 
    frame_count = int(worldVidCap.get(cv2.CAP_PROP_FRAME_COUNT))
    vidWidth  = worldVidCap.get(cv2.CAP_PROP_FRAME_WIDTH) #Get video height
    vidHeight = worldVidCap.get(cv2.CAP_PROP_FRAME_HEIGHT) #Get video width
    vidLength = range(frame_count)
    outputVid = cv2.VideoWriter('D:/Juggling/JSM/Juggling0003_06142020/EyeTracking/Calibration.mp4',-1,30,(int(vidWidth),int(vidHeight)))
    #Set HSV value (Hue, Saturation, Brightness) for color of ball
    lowerBound = np.array([160,135,135])
    upperBound = np.array([180,250,250])

    #Set an array for the calibration point
    calibPointXY = np.zeros(((endFrame-startFrame),2))
    for jj in vidLength:#For the length of the video
        if jj < startFrame:#If frame is before the start of calibration dont do anything
            success,image = worldVidCap.read()#reads in frame
            continue
        elif jj >= endFrame:#If frame is after calibration end the for loop
            break
        else: #If frame is in calibration range
            success,image = worldVidCap.read()#reads in frame
            #convert BGR to HSV
            imgHSV= cv2.cvtColor(image,cv2.COLOR_BGR2HSV) 
            mask=cv2.inRange(imgHSV,lowerBound,upperBound)
            #Clean up stray dots and fill in gaps 
            maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
            maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
            #Draw a contour with mask
            maskFinal=maskClose
            conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
            k=0
            objInFrame = []
            if jj == startFrame:
                plt.imshow(image)
                point = plt.ginput(1)
                point = point[0]
                normPoint = np.sqrt((point[0]**2 + point[1]**2))
                diffFromPointtoCont = 1000000
                for ii in range(len(conts)):
                    center, radius = cv2.minEnclosingCircle(conts[ii])
                    normCenter = np.sqrt(int(center[0])**2 + int(center[1])**2)
                    if abs(normCenter - normPoint) < diffFromPointtoCont:
                        diffFromPointtoCont = abs(normCenter - normPoint)
                        contIndex = ii
                        centerPoint = normCenter
                objInFrame.append(jj)
            else:
                #If contour is detected(Object is in frame) conts is true
                #Loop to output center position
                #for i in range(len(conts)):
                diffCenter = 100000000000
                diffRadius = 100000000000
                for i in range(len(conts)):
                    center, radius = cv2.minEnclosingCircle(conts[i])
                    centerx = int(center[0])
                    centery = int(center[1])
                    newNormCenter = np.sqrt(centerx**2 + centery**2)
                    radiusChange = abs(radius - radiusFromLastFrame)
                    
                    #print(radiusChange,'RadiusChange')
                    #if abs(newNormCenter - centerPoint) < diffCenter and abs(newNormCenter - centerPoint) <30 and radiusChange <diffRadius:
                    if  abs(newNormCenter - centerPoint) <60 and radiusChange <diffRadius and radius > 35:
                        diffCenter = abs(newNormCenter - centerPoint)    
                        diffRadius = radiusChange
                        #print(diffRadius,'DiffRadius')
                        calibPointXY[(jj-startFrame),0] = centerx
                        calibPointXY[(jj-startFrame),1] = centery
                        contIndex = i
                        #print(diffCenter)
                        objInFrame.append(i)
                #print('NEW FRAME')
            
            if len(objInFrame) >0:
                center,radius = cv2.minEnclosingCircle(conts[contIndex])
                centerPoint = np.sqrt(int(center[0])**2 + int(center[1])**2)
                radiusFromLastFrame = radius
                calibCont = conts[contIndex]
                cv2.drawContours(image,calibCont,-1,(255,0,0),3)
        # cv2.imshow('im',image)
        # cv2.waitKey(200)
            
            

    worldVidCap.release()
    #Reset worldVidcap
    worldVidCap = cv2.VideoCapture(worldVidPath)              
    for jj in vidLength:#For the length of the video
        if jj < startFrame:#If frame is before the start of calibration dont do anything
            success,image = worldVidCap.read()
            continue
        elif jj >= endFrame:#If frame is after calibration end the for loop
            break
        else: #If frame is in calibration range
            success,image = worldVidCap.read()
        #Make the pixel of the center point red
        cv2.circle(image,(int(calibPointXY[(jj-startFrame),0]),int(calibPointXY[int(jj-startFrame),1])),radius = 3, color =[255,0,0], thickness =-1)
        #image[int(calibPointXY[int(jj-startFrame),1]),int(calibPointXY[int(jj-startFrame),0]),:] = [0,0,255]
        if (jj - startFrame) >1:
            #Make the pixel of the center point of a previous frame red
            #image[int(calibPointXY[((jj-1)-startFrame),1]),int(calibPointXY[((jj-1)-startFrame),0]),:] = [0,0,255]
            cv2.circle(image,(int(calibPointXY[int((jj-1)-startFrame),0]),int(calibPointXY[int((jj-1)-startFrame),1])),radius = 3, color =[255,0,0], thickness =-1)

        if (jj - startFrame) >2:
            #Make the pixel of the center point of a previous frame red
            #image[int(calibPointXY[((jj-2)-startFrame),1]),int(calibPointXY[((jj-2)-startFrame),0]),:] = [0,0,255]
            cv2.circle(image,(int(calibPointXY[int((jj-2)-startFrame),0]),int(calibPointXY[int((jj-2)-startFrame),1])),radius = 3, color =[255,0,0], thickness =-1)

        if (jj - startFrame) >3:
            #Make the pixel of the center point of a previous frame red
            #image[int(calibPointXY[((jj-3)-startFrame),1]),int(calibPointXY[((jj-3)-startFrame),0]),:] = [0,0,255]
            cv2.circle(image,(int(calibPointXY[int((jj-3)-startFrame),0]),int(calibPointXY[int((jj-3)-startFrame),1])),radius = 3, color =[255,0,0], thickness =-1)

        if (jj - startFrame) >4:
            #Make the pixel of the center point of a previous frame red
            #image[int(calibPointXY[((jj-4)-startFrame),1]),int(calibPointXY[((jj-4)-startFrame),0]),:] = [0,0,255]
            cv2.circle(image,(int(calibPointXY[int((jj-4)-startFrame),0]),int(calibPointXY[int((jj-4)-startFrame),1])),radius = 3, color =[255,0,0], thickness =-1)

        if (jj - startFrame) >5:
            #Make the pixel of the center point of a previous frame red
            #image[int(calibPointXY[((jj-5)-startFrame),1]),int(calibPointXY[((jj-5)-startFrame),0]),:] = [0,0,255]
            cv2.circle(image,(int(calibPointXY[int((jj-5)-startFrame),0]),int(calibPointXY[int((jj-5)-startFrame),1])),radius = 3, color =[255,0,0], thickness =-1)
        if (jj - startFrame) >6:
            #Make the pixel of the center point of a previous frame red
            #image[int(calibPointXY[((jj-6)-startFrame),1]),int(calibPointXY[((jj-6)-startFrame),0]),:] = [0,0,255]
            cv2.circle(image,(int(calibPointXY[int((jj-6)-startFrame),0]),int(calibPointXY[int((jj-6)-startFrame),1])),radius = 3, color =[255,0,0], thickness =-1)

        #cv2.imshow('im',image)
        #cv2.waitKey(200)    
        outputVid.write(image)
    outputVid.release()
    #plt.imshow(image)
    #calibCorners = plt.ginput(4)
        
    #imgGrey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #points = cv2.cornerEigenValsAndVecs(imgGrey,calibCorners)









