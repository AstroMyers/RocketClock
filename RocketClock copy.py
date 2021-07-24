from typing import Text
import requests
import json

url =  "https://ll.thespacedevs.com/2.2.0/launch/upcoming/?is_crewed=false&include_suborbital=true&related=false&hide_recent_previous=true" #api to get info from
response = requests.get(url)
launch_info = json.loads(response.text) #get json with info

provider = []
mission = []
status = []
location = [] 
time = []
data = []


def UpdateLaunch(url): #ping API once to update to newest upcoming launch values

    global data_str
    print("Fetching Data")
    response = requests.get(url)
    launch_info = json.loads(response.text)
    for i in range(4):
        provider.append(launch_info['results'][i]['launch_service_provider']['name'])
        mission.append(launch_info['results'][i]['name'])
        status.append(launch_info['results'][i]['status']['name'])
        location.append(launch_info['results'][i]['pad']['name']+ ', ' + launch_info['results'][i]['pad']['location']['name'])
        time.append(launch_info['results'][i]['net'])
    
    for i in range(4):
        data.append(provider[i])
        data.append(mission[i])
        data.append(status[i])
        data.append(location[i])
        data.append(time[i])
        
        
    data_str = ' '.join(data)
        
    #time_list = list(time) #str -> list
    #time_list[10] = ' ' #remove characters
    #time_list[19] ='' #remove characters
    #time_format = ''.join(time_list) #list -> str
    #time_date = datetime.strptime(time_format,'%Y-%m-%d %H:%M:%S') #str -> date obj
    #data = [provider,mission,location, status,time]
    #data_str = ' '.join(data)
    #width,ignore = font.getsize(data_str)
    #return time_date, time_format, provider, mission, status, launch_info, data, data_str, width

UpdateLaunch(url)
print(data_str)