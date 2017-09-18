# USAGE
# python detect_sleeping.py 

# import the necessary packages
from multiprocessing import Process
from scipy.spatial import distance as dist
from imutils import face_utils
import imutils
import time
import dlib
import cv2
import sys

def restart_line():
#    Replaces a line printed on command line
    sys.stdout.write('\r')
    sys.stdout.flush()
    
def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear
 
def main_sleeping():
    # start the video stream 
    camera = cv2.VideoCapture(0)
    time.sleep(1.0)
    

    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
     
    # set variables   
    EYE_AR_THRESH = 0.3
    EYE_AR_CONSEC_FRAMES = 10
    COUNTER= 0
    state=""
    counter=0
    text= "Child not moving"
    
    # initialize the first frame in the video stream
    firstFrame = None
    
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]    
    
    
    # loop over frames from the video stream
    while True:
        (grabbed, frame) = camera.read()
        
        frame = cv2.flip(frame,1)
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        # detect face in the grayscale frame
        rects = detector(gray, 0)
        Eyes_Visible=False
    

        for rect in rects:
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
    
            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
    
            # average the eye aspect ratio together for both eyes
            ear = (leftEAR + rightEAR) / 2.0
    
            # check to see if the eye aspect ratio is below the blink
            # threshold, and if so, increment the blink frame counter
            if ear < EYE_AR_THRESH:
                COUNTER += 1
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    state="sleeping" 
                else:
                    state="awake"
    
            # otherwise, the eye aspect ratio is not below the blink
            # threshold
            else:
                # if the eyes were closed for a sufficient number of
                # then increment the total number of blinks
                state="awake"
                # reset the eye frame counter
                COUNTER = 0
    
            # draw the total number of blinks on the frame along with
            # the computed eye aspect ratio for the frame
            Eyes_Visible=True
            cv2.putText(frame, state, (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
            
        # show the frame
        if (not Eyes_Visible):
            cv2.putText(frame, "Eyes not visible", (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        gray1 = cv2.GaussianBlur(gray, (21, 21), 0)
        gray1 = cv2.GaussianBlur(gray, (7, 7), 0)
        
        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray1
            continue
        
        # compute the absolute difference between frames
        frameDelta = cv2.absdiff(firstFrame, gray1)
        #print (frameDelta.max(),frameDelta.mean())
        thresh = frameDelta.max()
        firstFrame = gray1
        
        if thresh>15:
            counter+=1
            if counter>10:
                text = "Child is moving"
        else:
            counter=0
            text= "Child not moving"
        
        # draw the text and timestamp on the frame
        cv2.putText(frame, text, (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            
        cv2.imshow("Child Video Feed", frame)
     
        # if the `q` key was pressed, break from the loop
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    
    # do a bit of cleanup
    camera.release()
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    Process(target=main_sleeping).start()