# EyeTracking
# EyeTracking.py preprocesses video data from pupil labs eye tracker in order to make the data more feasible to work with.
# There are multiple functions in the file that for the most part only need the filepath for eyetracking and world view videos
#
# reEncodeVids Function: Input is the filepath for the pupil labs videos and a list of the fps of the views in order of world, eye0,eye1
# The function takes each frame from the pupil lab videos and then creates a new video with those frames with a H264 codec.
# Videos are saved with the same input filename with '_f' added at the end of it  
# This is done to create videos that are easier to work with.
#
# FlashDetection Function: Input for function is the pupil labs video filepath
# Function finds the flash bulb at beginnning and end of the video and returns the frame number where the flash occurs.
#
# TrimVideos: Input for function is the pupil labs video filepath and the two varibales returned from the flash detection function
# This function trims the videos to start at the first flash and and end at the second flash
# Videos are saved with the same input filename with '_c' added at the end of it  
#
# ginput function: Input for function is pupil labs video filepath.
# Function opens up the frames of the video and allows the user to click on pixels and the coordinates of those pixels are saved.
