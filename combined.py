# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 22:13:55 2017

@author: Kanchana
"""

from multiprocessing import Process,Manager
from scipy.spatial import distance as dist
from imutils import face_utils
import imutils
import time
import dlib
import cv2

from detect_sleeping import eye_aspect_ratio,main_sleeping
from sound_detect import restart_line,sound_main
from Database import update_Database


if __name__ == '__main__':
    #manager = Manager()
    
    #dataArray = manager.list()
    #print dataArray
    Process(target=sound_main).start()  
    Process(target=main_sleeping).start()
    #Process(target=update_Database).start()

    
