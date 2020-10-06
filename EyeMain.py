import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
from matplotlib import animation
import ffmpeg
import skvideo.io
import pandas as pd
import math
from skimage import morphology, measure
import scipy
from EyeTracking import reEncodeVids, flashDetection, trimVids, saveTimeStamps, plotVideosTogether
from scatteredInterpolantCalibration import scatteredInterpolantCalibrationTrack, Interpolate
from PupilTracking import PupilTrack

#Base path where all videos are saved
videosFilePath = 'D:/MoCapNEU/EyeTrackTesting/2020_10_05/000'

#In order of [world, eye0,eye1]
vidfps = [120,123,123]
worldVideoName = 'world'
eye1VideoName = 'eye0'
eye2VideoName = 'eye1'

#Frame #s where the calibration takes place
startFrame = 2000
endFrae = 2500

eyeVideoNames = [eye1VideoName, eye2VideoName]
videoNames  = [worldVideoName, eye1VideoName, eye2VideoName]

reEncodeVids(videosFilePath,videoNames, vidfps)

startFlash, endFlash = flashDetection(videosFilePath,videoNames)

trimVids(videosFilePath,videoNames, startFlash, endFlash)

saveTimeStamps(videosFilePath, videoNames)

pupilCenter = PupilTrack(videosFilePath,eyeVideoNames)

calibPointXY, scatteredInterpolantCalibrationTrack(videosFilePath, videoNames, startFrame, endFrame)

eyeFocusPoints = Interpolate(pupilCenter, calibPointXY, startFrame, endFrame)
