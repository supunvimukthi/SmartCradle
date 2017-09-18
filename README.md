# SmartCradle

Device to monitor a baby in cradle

## Requirements

Raspberry Pi 3
Webcam/Microphone
Python: imutils/dlib/cv2

## Implementation
combined.py is the main file. Ensure other files are in same folder. 
Currently tested for windows. Simply run on cmd, and visual and audio detection systems will run. 
'q' should break the video process. 
use ctrl+c to break sound loop. 


## Dependencies
sound_detect.py checks if background sound is detected. Run on cmd, and use ctrl+c to break loop.
detect_sleeping.py handles the vision component. Run on cmd, and use 'q' to break loop.