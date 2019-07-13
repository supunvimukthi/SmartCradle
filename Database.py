import time
import requests
import json
firebase_url = 'https://childcare-1658e.firebaseio.com/'

def update_Database(dataArray):
    sleep=detect_sleep(dataArray[0],dataArray[1],dataArray[2])
    write_to_firebase_video(sleep)
    write_to_firebase_audio(dataArray[2])
    
def write_to_firebase_video(value):
    firebase_url = 'https://childcare-1658e.firebaseio.com/'
    data = {'sleeping':value}
    try:
         result=requests.put(firebase_url + '/' + 'Child Care' + '/video.json', data=json.dumps(data))
#        print ('Record inserted. Result Code = ' + str(result.status_code) + ',' + result.text)
    except IOError:
        pass
#        print ('error')


def write_to_firebase_audio(value):
    firebase_url = 'https://childcare-1658e.firebaseio.com/'
    data = {'sound':value}
    try:
        requests.put(firebase_url + '/' + 'Child Care' + '/audio.json', data=json.dumps(data))
    except IOError:
        pass
  
def detect_sleep(babyEyes,moving,makeSounds):
     #int babyEyes = 1    # 0-babyEyesCantBeSeen 1-babyEyesClosed 2- Open
     #int makeSounds = 1  # 0- no sound 1-anysound 2- cryingSound
     #int moving = 1
     sleeping = 0
     sleep_array=[]
     if babyEyes==1:
          sleeping =1
     elif babyEyes ==2:
          sleeping =0
     elif babyEyes==0:
          if makeSounds==0 and moving==0:
               sleeping =1
          elif moving==1 and makeSounds==1:
               sleeping =0
          elif makeSounds ==2:
               sleeping =0
     sleep_array.append(sleeping)
     return sleeping
if __name__ == '__main__':
    Process(target=update_Database).start()
