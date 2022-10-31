import requests, json, os, platform, math
from time import sleep
from mpl_toolkits.basemap import Basemap
from datetime import datetime   
import matplotlib.pyplot as plt
import numpy as np

#To do list
# - Fix the plot blocking the countdown timer
# - Convert UTC/GMT to local time 

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
    url =  "https://ll" + dev + '.thespacedevs.com/2.2.0/launch/upcoming/?include_suborbital=true&hide_recent_previous=true'
    os.system(reset)
    return url, reset
    
def UpdateLaunch(url): #ping API once to update to newest upcoming launch values
    time = []
    response = requests.get(url)
    launch_info = json.loads(response.text)
    
    for i in range(0,len(launch_info)):
        if launch_info['results'][i]['pad']['location']['country_code'] != 'USA':
            pass
        elif launch_info['results'][i]['pad']['location']['country_code'] == 'USA':
            provider = launch_info['results'][i]['launch_service_provider']['name']
            mission =launch_info['results'][i]['name']
            status = launch_info['results'][i]['status']['name']
            location = launch_info['results'][i]['pad']['name'] + ', ' + launch_info['results'][i]['pad']['location']['name']
            latitude =  launch_info['results'][i]['pad']['latitude']
            longitude =  launch_info['results'][i]['pad']['longitude']
            window_start = launch_info['results'][i]['window_start']
            window_end = launch_info['results'][i]['window_end']
            time = launch_info['results'][i]['net']
            break
    
    
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
    fig = plt.figure(figsize=(7,4))
    
    m = Basemap(projection='merc',
           llcrnrlat = 23,
           urcrnrlat = 53,
           llcrnrlon = -130,
           urcrnrlon = -60,
           resolution = 'c')
    
    longitude, latitude = round(longitude, 2), round(latitude, 2)
    location = location.split(", ")
    
    if longitude > 0: 
        longpos = chr(176) +'E'
    elif longitude < 0: 
        longpos = chr(176) +'W'
    elif longitude > 180 or longitude < -180:
        print('Invalid Longitude')
    
    if latitude > 0: 
        latpos = chr(176) +'N'
    elif latitude < 0:
        latpos = chr(176) + 'S'
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
    m.drawstates(linewidth = 1)
    m.plot(x_long, y_lat, 'wo', markeredgecolor = 'black', markeredgewidth = '2', markersize = '7')
    
    plt.vlines(x_long, min_y, max_y, color = 'red', linestyles = 'dashed' )
    plt.hlines(y_lat, min_x, max_x, color = 'red', linestyles = 'dashed')
    plt.text(x_long + 100000, y_lat +  550000,f'{location[0]}',color = 'white', size = 'small')
    plt.text(x_long + 100000, y_lat +  350000,f'{location[1]}', color = 'white', size = 'small')
    plt.text(x_long + 100000, y_lat +  150000,f'{str(abs(latitude))+ latpos}, {str(abs(longitude))+ longpos}' ,color = 'white', size = 'small')
    #plt.title(str(location), fontsize='15')
    plt.draw()
    plt.pause(5)

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
    main(deltatime, reset, url, location, longitude, latitude)
    
def main(deltatime, reset, url, location, longitude, latitude):
    Location(location, float(longitude), float(latitude)) #for now can't really get this to work without blocking the countdown timer :(
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