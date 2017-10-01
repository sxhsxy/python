# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 10:31:24 2016

@author: xiaohu
"""

import os
import time
import datetime
import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  #用来正常显示负号


url = "http://www.tmsf.com/upload/report/mrhqbb/{}/xf.html"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
# x = pd.read_html(url, header=0)
date_l = pd.date_range(start="20170101", end="20170521", freq='1D')
r = requests.get(url.format('20170101'), headers=headers)
x = pd.read_html(r.text, header=0)
area_day = x[2]
col = area_day.loc[:, '区域']
result = pd.DataFrame(index=date_l, columns=col)
# time.sleep(3)
for date in date_l:
    url_day = url.format(datetime.datetime.strftime(date, '%Y%m%d'))
    print(url_day)
    attemp = 0
    while attemp < 5:
        try:
            r = requests.get(url_day, headers=headers)
            x = pd.read_html(r.text, header=0)
            area_day = x[2]
            # print(area_day)
            quantity_area_day = area_day.loc[:, ['区域','可售套数（套）']]
            col = area_day.loc[:, '区域']
            data = area_day.loc[:, '可售套数（套）']
            data.index = quantity_area_day.iloc[:, 0]
            result.loc[date] = data
            # time.sleep(2)
            break
        except Exception as e:
            attemp += 1
            print("retry {}: {}".format(attemp, e))
            time.sleep(2*attemp)
            continue
