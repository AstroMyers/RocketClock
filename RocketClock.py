from typing import Text
import requests
import json
from datetime import datetime
import time as tic
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from random import randrange
from rgbmatrix import RGBMatrix, RGBMatrixOptions

# matrix configuration
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.hardware_mapping = 'adafruit-hat-pwm'
options.gpio_slowdown = 4
matrix = RGBMatrix(options = options)

url =  "https://ll.thespacedevs.com/2.2.0/launch/upcoming/?is_crewed=false&include_suborbital=true&related=false&hide_recent_previous=true" #api to get info from
font = ImageFont.truetype("/home/pi/rpi-rgb-led-matrix/bindings/python/samples/arial.ttf",26)

def Loop():
    red = randrange(0,256)
    blue = randrange(0,256)
    green = randrange(0,256)
    color = (red,green,blue)
    image= Image.new("RGB",(width+30,32))
    x=0
    print("Looping")
    draw = ImageDraw.Draw(image)
    draw.text((x,0),data_str, font=font,fill = color, align = 'left')
    x = x + width
    for i in range(-128,width):
        matrix.Clear()
        matrix.SetImage(image, -i, 0)
        tic.sleep(.03)
    matrix.Clear()

def UpdateLaunch(url): #ping API once to update to newest upcoming launch values
    global data_str
    global width
    
    mission = []
    status = []
    time = []
    location = []
    data = []
    provider = []

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
    
    width,ignore = font.getsize(data_str)
    print('Looping')
    Loop()
    return time, provider, mission, status, launch_info, data, data_str, width

while True:
  
    UpdateLaunch(url)
    tic.sleep(300)