# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 00:09:14 2023

@author: marie
"""
from datetime import datetime 
import pandas as pd

def get_voltage(url = 'http://192.168.2.6/api/v1/p1port/telegram', timestamp = True):
    import json
    import requests

    result = requests.get(url)
    telegram = json.loads(result.text)
    parts = telegram[3].split('\n')
    for part in parts:
        if 'V' in part:
            return [float(part.split('(')[1].split('*')[0]), datetime.strptime(telegram[0], "%Y-%m-%d %H:%M:%S")]
            break
        
s = pd.Series(dtype = float)
while True:
    voltage, time = get_voltage()
    s[time] = voltage
