import cv2
import numpy as np 
#from matplotlib import pyplot as plt 
import time

# gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
# Defaults to 1280x720 @ 60fps
# Flip the image by setting the flip_method (most common values: 0 and 2)
# display_width and display_height determine the size of the window on the screen

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )
beginTime = time.time()




#Open Camera
cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fourcc = cv2.VideoWriter_fourcc(*'H264')

out = cv2.VideoWriter('/media/chris/SSD500/test.mp4',fourcc, 30, (frame_width,frame_height))
timestampsList = []

while(True):
    #grab frame
    ret,frame = cap.read()
    print(ret)
    if ret:
        #Write to output file
        out.write(frame)
        timestampsList.append(time.time() - beginTime)
        cv2.imshow('im',frame)
        if cv2.waitKey(1) & 0xFF ==ord('q'):
            break


cv2.destroyAllWindows()
diffFrames = np.diff(timestampsList)
frames = range(len(diffFrames))
#plt.scatter(frames, diffFrames, s=1)
#plt.xlabel('Frames')
#plt.ylabel('Time taken to write frame (s)')
#plt.title('Webcam writespeed at 30fps')
#plt.show()
