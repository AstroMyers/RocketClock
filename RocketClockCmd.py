from typing import Text
import requests
import json
from time import sleep
import os

url =  "https://lldev.thespacedevs.com/2.2.0/launch/upcoming/?is_crewed=false&include_suborbital=true&related=false&hide_recent_previous=true" #api to get info from
response = requests.get(url)
launch_info = json.loads(response.text) #get json with info

launch = []
provider = []
mission = []
status = []
location = [] 
time = []
data = []


def UpdateLaunch(url): #ping API once to update to newest upcoming launch values

    global data_str
    os.system('clear')
    response = requests.get(url)
    launch_info = json.loads(response.text)
    for i in range(4):
        provider.append(launch_info['results'][i]['launch_service_provider']['name'])
        mission.append(launch_info['results'][i]['name'])
        status.append(launch_info['results'][i]['status']['name'])
        location.append(launch_info['results'][i]['pad']['name']+ ', ' + launch_info['results'][i]['pad']['location']['name'])
        time.append(launch_info['results'][i]['net'])
    
    for i in range(4):
        launch = [provider[i], mission[i], status[i], location[i], time[i]]
        
        print('Provider: ' + launch[0])
        print('Mission: ' + launch[1])
        print('Status: ' + launch[2])
        print('Location: ' + launch[3])
        print('Time: ' + launch[4])
        print('\n')
        launch.append(launch)
        sleep(10)
    
        
        
        
    #data_str = ' '.join(data)
        
    #time_list = list(time) #str -> list
    #time_list[10] = ' ' #remove characters
    #time_list[19] ='' #remove characters
    #time_format = ''.join(time_list) #list -> str
    #time_date = datetime.strptime(time_format,'%Y-%m-%d %H:%M:%S') #str -> date obj
    #data = [provider,mission,location, status,time]
    #data_str = ' '.join(data)
    #width,ignore = font.getsize(data_str)
    #return time_date, time_format, provider, mission, status, launch_info, data, data_str, width

os.system('clear')
UpdateLaunch(url)
#print(data_str)
