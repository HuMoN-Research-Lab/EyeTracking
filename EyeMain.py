from EyeTracking import reEncodeVids, flashDetection, trimVids, saveTimeStamps, plotVideosTogether
from scatteredInterpolantCalibration import scatteredInterpolantCalibrationTrack, Interpolate
from PupilTracking import PupilTrack

#Base path where all videos are saved
videosFilePath = 'E:/MoCapNEU/EyeTrackTesting/2020_10_08/002'

#In order of [world, eye0,eye1]
vidfps = [120,120,120]
worldVideoName = 'world'
eye1VideoName = 'eye0'
eye2VideoName = 'eye1'

#Frame #s where the calibration takes place
startFrame = 1200
endFrame = 2760

eyeVideoNames = [eye2VideoName]
videoNames  = [worldVideoName, eye1VideoName, eye2VideoName]

#reEncodeVids(videosFilePath,videoNames, vidfps)

#startFlash, endFlash = flashDetection(videosFilePath,videoNames)

#trimVids(videosFilePath,videoNames, startFlash, endFlash)

#saveTimeStamps(videosFilePath, videoNames)

#pupilCenter = PupilTrack(videosFilePath,eyeVideoNames)

#calibPointXY = scatteredInterpolantCalibrationTrack(videosFilePath, videoNames, startFrame, endFrame)
pupilCenter = np.load(videosFilePath+'/eye0_pupilTrack.npy')
calibPointXY = np.load(videosFilePath+'/CalibLocXY.npy')
eyeFocusPoints = Interpolate(videosFilePath,videoNames,pupilCenter, calibPointXY, startFrame, endFrame)
