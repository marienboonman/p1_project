# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 00:09:14 2023

@author: marie
"""
from datetime import datetime 
import pandas as pd
import time

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
        

while True:
    s = pd.Series(dtype = float, name = 'Spanning (V)')
    voltage, timestamp = get_voltage()
    n = 0
    while True:
        voltage, timestamp = get_voltage()
        if timestamp.second%10 == 0:
           s[timestamp] = voltage
           time.sleep(7)
           n = n+1
           #print('added')
           if n == 1:
               starttime = timestamp
        #else:
        #   print('waiting')
       
        if n == 9:
           endtime = timestamp
           filename = ('data/data from {} to {}.csv'.format(starttime, endtime))
           s.to_csv(filename.replace(':','-'))
           break
