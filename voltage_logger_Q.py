# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 00:09:14 2023

@author: marie
"""
from datetime import datetime 
import pandas as pd
import time
import sys
import os

try:
    rep = int(sys.argv[1])
except:
    rep = 6*15

try:
    folder = sys.argv[2]
except:
    print('Invalid or no folder name specified')

if not folder in os.listdir():
    os.system('mkdir {}'.format(folder))

def get_voltage(url = 'http://{}/api/v1/p1port/telegram', ip = '192.168.2.6' ,timestamp = True):
    import json
    import requests

    url = url.format(ip)    
    result = requests.get(url)
    telegram = json.loads(result.text)
    parts = telegram[3].split('\n')
    for part in parts:
        if 'V' in part:
            return [float(part.split('(')[1].split('*')[0]), datetime.strptime(telegram[0], "%Y-%m-%d %H:%M:%S")]
            break
        


s = pd.Series(dtype = float, name = 'Spanning (V)')
voltage, timestamp = get_voltage()
n = 0
while True:
    try:
        voltage, timestamp = get_voltage()
        if timestamp.second%10 == 0:
            s[timestamp] = voltage
            time.sleep(8)
            n = n+1
            if n == 1:
                starttime = timestamp
    
        if n == rep:
            endtime = timestamp
            filename = ('{}/data_from_{}_to_{}.csv'.format(folder, starttime, endtime))
            s.to_csv(filename.replace(':','-').replace(' ','_'))
            break
    except:
        print('Polling failed at {}'.format(str(datetime.now())))