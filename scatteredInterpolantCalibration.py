import numpy as np
import cv2


worldVidPath = 'C:\Users\chris\EyeTracking\Data\world_f.mp4'
eye0VidPath =  'C:\Users\chris\EyeTracking\Data\eye0.mp4'
eye1VidPath =  'C:\Users\chris\EyeTracking\Data\eye1.mp4'

worldVidCap = cv2.VideoCapture(worldVidPath)
eye0VidCap = cv2.VideoCapture(eye0VidPath)
eye1VidCap = cv2.VideoCapture(eye1VidPath)

startFrame = (NEED FRAME NUM)
endFrame = (NEED FRAME NUM)

frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
vidLength = range(frame_count)

#In Mat Lab Scfipt there is a while loop that takes every framne up to the start frame index
# not adding it yet cause i dont see its point

"""" When You go back into the remote desktop --- add the ginput finction  here"""

