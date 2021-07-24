import requests
import json
from time import sleep
import os
import platform
from datetime import datetime
import cartopy.crs as ccrs                # Mapping
import matplotlib.pyplot as plt 

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
    print(latitude,longitude)
    print('\n')
    
    plt.plot([float(longitude)], [float(latitude)], color='red', marker='o', markersize=6,transform=ccrs.PlateCarree())
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.stock_img()
    plt.show()
    Time(time)
    
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
    print('Launch Imminent!')
    sleep(5)
    os.system(reset)
    print('Retreiving Next Launch...')
    sleep(10)
    os.system(reset)
    UpdateLaunch(url)
    main()
    
def main():
    while True:
        while deltatime.total_seconds() < 1:
            Launch()
        while deltatime.total_seconds() > 1:
            Time(time)
            break

if __name__ == '__main__':
    Init()
    Time(time)
    main()