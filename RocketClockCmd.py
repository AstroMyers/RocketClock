import requests
import json
from time import sleep
import os
import platform
from datetime import datetime

def SystemDetect():
    global reset
    system = platform.system()
    if system == 'Windows':
        reset = 'cls'
    elif system == 'Linux':
        reset = 'clear'
    elif system == 'Darwin':
        reset  = 'clear'
    os.system(reset)
    print('System Detected: ',system)
    sleep(1)
    print('Fetching Data\n')
    sleep(1)
    return reset

def Init():
    global url
    SystemDetect()
    mode = input('Press 1 for Dev Mode or 2 for Live Mode:\n')
    if mode == '1':
        dev = 'dev'
    elif mode == '2':
        dev = ''
    url =  "https://ll" + dev + '.thespacedevs.com/2.2.0/launch/upcoming/?is_crewed=false&include_suborbital=true&related=false&hide_recent_previous=true' #api to get info from
    os.system(reset)
    UpdateLaunch(url)
    sleep(1)
    return url
    
def UpdateLaunch(url): #ping API once to update to newest upcom2ing launch values
    global time
    time = []
    response = requests.get(url)
    launch_info = json.loads(response.text)
    provider = launch_info['results'][0]['launch_service_provider']['name']
    mission =launch_info['results'][0]['name']
    status = launch_info['results'][0]['status']['name']
    location = launch_info['results'][0]['pad']['name']+ ', ' + launch_info['results'][0]['pad']['location']['name']
    time = launch_info['results'][0]['net']
    print('Provider: ', provider)
    print('Mission: ', mission)
    print('Status: ', status)
    print('Location: ', location)
    print('Time: ', time)
    print('\n')
    return time
    
def Time(time):
    global deltatime
    time_list = list(str(time)) #str -> list
    time_list[10] = ' ' #remove characters
    time_list[19] ='' #remove characters
    time_format = ''.join(time_list) #list -> str
    time_date = datetime.strptime(time_format,'%Y-%m-%d %H:%M:%S') #str -> date obj
    now = datetime.utcnow()
    deltatime =  time_date - now
    print('Countdown: ' + str(deltatime), end='\r')
    return deltatime
    
def Launch():
    os.system(reset)
    print('Launching!')
    sleep(.5)
    print('Launching!')
    sleep(.5)
    print('Launching!')
    sleep(3)
    os.system(reset)
    print('Retreiving Next Launch...')
    sleep(3)
    UpdateLaunch(url)
    
def main():
    while True:
        while deltatime.total_seconds() < 1:
            Launch()
            break
        while deltatime.total_seconds() > 1:
            Time(time)
            break

if __name__ == '__main__':
    Init()
    Time(time)
    main()