import requests, json, os, platform, math
from time import sleep
from mpl_toolkits.basemap import Basemap
from datetime import datetime   
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

matplotlib.use('TkAgg')
#this script was created to pull live upcoming rocket launch data and display it in a command line interface

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
    url =  "https://ll" + dev + '.thespacedevs.com/2.2.0/launch/upcoming/?include_suborbital=true&hide_recent_previous=true' #api to get info from
    os.system(reset)
    return url, reset
    
def UpdateLaunch(url): #ping API once to update to newest upcoming launch values
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
    
    def UTC_to_local():
        pass
    
    print('Provider:     ', provider)
    print('Mission:      ', mission)
    print('Status:       ', status)
    print('Location:     ', location)
    print('Time:         ', time)
    print('Window Start: ',window_start, '| Window End: ',window_end)
    print('Latitude:     ',latitude, '| Longitude: ',longitude)
    print('\n')
    Time(time)
    return time, location, longitude, latitude

def Location(location, longitude, latitude):
    longitude, latitude = round(longitude, 2), round(latitude, 2)
     
    fig = plt.figure(figsize=(12,9))
    
    m = Basemap(projection='merc',
           llcrnrlat = -70,
           urcrnrlat = 70,
           llcrnrlon = -180,
           urcrnrlon = 180,
           resolution = 'c')
    
    if longitude > 0: 
        longpos = 'E'
    elif longitude < 0: 
        longpos = 'W'
    elif longitude > 180 or longitude < -180:
        print('Invalid Longitude')
    
    if latitude > 0: 
        latpos = 'N'
    elif latitude < 0:
        latpos = 'S'
    elif latitude > 80 or latitude < -80:
        print('Invalid Latitude')
    
    x_long, y_lat = m(longitude, latitude)
    max_x, max_y = m(180, 80)
    min_x, min_y = m(-180,-80)
    
    m.bluemarble(scale = 0.5)
    m.drawparallels(np.arange(-90,90,10),linewidth ='0',labels=[True,False,False,False])
    m.drawmeridians(np.arange(-180,180,30),linewidth ='0',labels=[0,0,0,1])
    m.drawcountries(linewidth = 1)
    m.drawcoastlines(linewidth = 1)
    m.plot(x_long, y_lat, 'ro', markeredgecolor = 'black', markeredgewidth = '2', markersize = '7')
    
    plt.vlines(x_long, min_y, max_y, color = 'red', linestyles = 'dashed' )
    plt.hlines(y_lat, min_x, max_x, color = 'red', linestyles = 'dashed')
    plt.text(x_long + 500000, y_lat + 500000,f'{str(abs(latitude))+latpos}, {str(abs(longitude))+longpos}', color = 'white')
    plt.title(str(location), fontsize='15')
    plt.draw()
    plt.pause(0.0001)

def Time(time):
    time = time.replace('Z', '')
    time = time.replace('T',' ')
    time_date = datetime.strptime(time,'%Y-%m-%d %H:%M:%S') #str -> date obj
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
    sleep(5)
    os.system(reset)
    UpdateLaunch(url)
    main()
    
def main(deltatime, reset, url, location, longitude, latitude):
    #Location(location, float(longitude), float(latitude)) for now can't really get this to work without blocking the countdown timer :(
    while True:
        while deltatime.total_seconds() < 1:
            Launch(reset, url)
        while deltatime.total_seconds() > 1:
            Time(time)
            break

if __name__ == '__main__':
    url, reset = Init()
    time, location, longitude, latitude = UpdateLaunch(url)
    deltatime = Time(time)
    main(deltatime, reset, url,location, longitude, latitude)