# EyeTracking
   Repository takes video from an eyetracker with videos on each eye and one the records the world view. In this recording the user uses a flash bulb
   to sync the videos and there is a section of time where the user holds out a ball and moves it throughout the frame in order to calibrate the cameras.
   The repository then utilizes this information to get the location where the eye was looking in the world view camera.
   
 EyeMain.py
   Pipeline that strings together all functions. The raw videos are reencoded and then trimmed. The trimmed videos are then proceesed to find pupil location
   throughout the video and ball location when calibrating. The ball location is then used to interpolate a function that maps the eye location onto the 
   world view video, which is where the eye was gazing. 
 
 EyeTrackingHelperFunctions.py 
    Functions that mainly preprocesses and flash syncs video data from pupil labs eye tracker in order to make the data more feasible to work with.
    There are multiple functions in the file that for the most part only need the filepath for eyetracking and world view videos

    reEncodeVids Function: Input is the filepath for the pupil labs videos and a list of the fps of the views in order of world, eye0,eye1
    The function takes each frame from the pupil lab videos and then creates a new video with those frames with a H264 codec.
    Videos are saved with the same input filename with '_f' added at the end of it  
    This is done to create videos that are easier to work with.

    FlashDetection Function: Input for function is the pupil labs video filepath
    Function finds the flash bulb at beginnning and end of the video and returns the frame number where the flash occurs.

    TrimVideos: Input for function is the pupil labs video filepath and the two varibales returned from the flash detection function
    This function trims the videos to start at the first flash and and end at the second flash
    Videos are saved with the same input filename with '_c' added at the end of it  

    ginput function: Input for function is pupil labs video filepath.
    Function opens up the frames of the video and allows the user to click on pixels and the coordinates of those pixels are saved.

 PupilTracking.py
    Takes both eye videos and tracks the center of pupil throughout each video. Data is stored in a numpy array and saved to the 
    same filepath as videos. A video of the tracked pupil is also created
 
 scatteredInterpolationCalibration.py
    
    scatteredInterpolantCalibrationTrack: Along with the world video filepath, the first and last frame number of when calibration takes place needs to be input into the function.
    The calibration is where a bright colored ball is held out and moved across the field of view of the world camera. The function tracks the center of the ball and saves the data 
    in a npy file in the same filepath as the videos. A video of the ball being tracked is also created

    interpolate: The inputs to this function is the file path of all videos and their respective videonames, the start and end frame where the calibration takes place,
    and the numpy array of the pupil location and location of ball throuhgout the calibration section. The pupil location and ball location during the calibration section 
    are then put into a interpolator that cretes a function to map the pupil location into the real world where the eye was gazing. A video of the real world with a marker
    over the gaze and an array of the gaze pixel location are created.
    
