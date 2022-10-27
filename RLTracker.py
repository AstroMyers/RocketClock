import requests
import json
from time import sleep
import os
import platform
from datetime import datetime               # Mapping
import matplotlib.pyplot as plt 

#!apt-get install libproj-dev proj-data proj-bin
#!apt-get install libgeos-dev
#!pip install cython
#pip install cartopy

def SystemDetect():
    system = platform.system()
    if system == 'Windows':
        reset = 'cls'
    elif system == 'Linux' or 'Darwin':
        reset = 'clear'
    os.system(reset)
    print('System Detected: ',system)
    print('Fetching Data\n')
    sleep(1)
    return reset

def Init():
    reset = SystemDetect()
    mode = input('Press 1 for Dev Mode or 2 for Live Mode:\n')
    if mode == '1':
        dev = 'dev'
    elif mode == '2':
        dev = ''
    url =  "https://ll" + dev + '.thespacedevs.com/2.2.0/launch/upcoming/?is_crewed=true&include_suborbital=true&related=false&hide_recent_previous=true' #api to get info from
    os.system(reset)
    sleep(1)
    return url, reset
    
def UpdateLaunch(url): #ping API once to update to newest upcom2ing launch values
    time = []
    response = requests.get(url)
    launch_info = json.loads(response.text)
    
    provider = launch_info['results'][0]['launch_service_provider']['name']
    mission =launch_info['results'][0]['name']
    status = launch_info['results'][0]['status']['name']
    location = launch_info['results'][0]['pad']['name'] + ', ' + launch_info['results'][0]['pad']['location']['name']
    latitude =  launch_info['results'][0]['pad']['latitude']
    longitude =  launch_info['results'][0]['pad']['longitude']
    window_start = launch_info['results'][0]['window_start']
    window_end = launch_info['results'][0]['window_end']
    time = launch_info['results'][0]['net']
    print('Provider: ', provider)
    print('Mission: ', mission)
    print('Status: ', status)
    print('Location: ', location)
    print('Time: ', time)
    print('Window Start: ',window_start, '| Window End: ',window_end)
    print('Latitude: ',latitude, '| Longitude: ',longitude)
    print('\n')
    Time(time)
    return time
    
def Time(time):
    time_list = list(str(time)) #str -> list
    time_list[10] = ' ' #remove characters
    time_list[19] ='' #remove characters
    time_format = ''.join(time_list) #list -> str
    time_date = datetime.strptime(time_format,'%Y-%m-%d %H:%M:%S') #str -> date obj
    now = datetime.utcnow()
    deltatime =  time_date - now
    print('Countdown: ' + str(deltatime), end='\r')
    return deltatime
    
def Launch(reset, url):
    os.system(reset)
    print('Launch Imminent!')
    sleep(5)
    os.system(reset)
    print('Retreiving Next Launch...')
    sleep(10)
    os.system(reset)
    UpdateLaunch(url)
    main()
    
def main(deltatime, reset, url):
    while True:
        while deltatime.total_seconds() < 1:
            Launch(reset, url)
        while deltatime.total_seconds() > 1:
            Time(time)
            break

if __name__ == '__main__':
    url, reset = Init()
    time = UpdateLaunch(url)
    deltatime = Time(time)
    main(deltatime, reset, url)