import time
import requests
import json
from firebase_admin import db
firebase_url = 'https://childcare-1658e.firebaseio.com/'

#Setup a loop to send Temperature values at fixed intervals
#in seconds
fixed_interval = 10
while 1:
  try:
    #temperature value obtained from Arduino + LM35 Temp Sensor          
    temperature_c = "FUCKss"
    t='Kss'
    
    #current time and date
    time_hhmmss = time.strftime('%H:%M:%S')
    date_mmddyyyy = time.strftime('%d/%m/%Y')
    
    #current location name
    temperature_location = 'Mumbai-Kandivali';
    print temperature_c + ',' + time_hhmmss + ',' + date_mmddyyyy + ',' + temperature_location
    
    #insert record
    data = {'date':date_mmddyyyy,'time':time_hhmmss,'value':temperature_c}
    result = requests.put(firebase_url + '/' + temperature_location + '/temperature.json', data=json.dumps(data))
    data = {'date':date_mmddyyyy,'time':time_hhmmss,'value':t}
    result1 = requests.put(firebase_url + '/' + temperature_location + '/temperatu.json', data=json.dumps(data))

    
    print 'Record inserted. Result Code = ' + str(result.status_code) + ',' + result.text
    time.sleep(fixed_interval)
  except IOError:
      print('Error! Something went wrong.')
  time.sleep(fixed_interval)
