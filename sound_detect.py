# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 22:37:33 2017

@author: Supun, Kanchana
"""

import pyaudio
import audioop
import sys
import time
#import cv2

CHUNK=1024
FORMAT=pyaudio.paInt16
CHANNELS=2
RATE=44100

THRESH = 1500
TIME_GAP=10

def restart_line():
#    Replaces a line printed on command line
    sys.stdout.write('\r')
    sys.stdout.flush()

def sound_main():
    p=pyaudio.PyAudio()
    #print p. get_default_host_api_info()
    #print p.get_default_input_device_info()
    #print p.get_device_info_by_index(2)
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=2)
    
    
    sys.stdout.write('started recording \n')
    sys.stdout.flush()
    time.sleep(1)

    counter=0
    counter2=0
    
    while True:
#        timeout = time.time()+20
        data = stream.read(CHUNK)
        rms = audioop.rms(data, 2)
        
        if rms>THRESH:
            counter+=1
            counter2=0
            if counter>TIME_GAP:
                restart_line()
                sys.stdout.write('Baby Awake             ')
                sys.stdout.flush() 
                counter=0
        else:
            counter=0
            counter2+=1
            if counter2>TIME_GAP:
                restart_line()
                sys.stdout.write('Baby Asleep         ')
                sys.stdout.flush() 
                counter2=0
           
#        if time.time>timeout:
#            break
    #    key = cv2.waitKey(1) & 0xFF
    #    if key == ord("q"):
    #        switch=False
    #        break
                
    print(" done recording")
    
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == '__main__':
    sound_main()
