# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 10:31:24 2016

@author: xiaohu
"""

import requests
import datetime
import time
import re
import json
import PyQt5.QtGui
import io
import PIL.Image
import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel


s= requests.Session()
root_url = "http://www.learning.gov.cn"
login_url = "http://www.learning.gov.cn/study/login.php"
ajax_url = "http://www.learning.gov.cn/study/ajax.php"
course_url = "http://www.learning.gov.cn/course/course.php"
index_url = root_url + "/index.php"
akey_url = root_url + "/system/akey_img.php"
post_data="act=AjaxLogin&username=339005198609279316&password=123456&islogin=0&authKey="

headers_str = """Connection: keep-alive
Content-Length: 80
Accept: application/json, text/javascript, */*; q=0.01
Origin: http://www.learning.gov.cn
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Referer: http://www.learning.gov.cn/index.php
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.8"""


def login():
    data = {'username':'320323197111221058', 'password':'19981226'}
    resp = s.post(login_url, data, allow_redirects=False)
    resp.encoding = 'utf-8'
    print(resp.status_code)
    print(resp.headers)
    print(resp.text)
    if 'profile' in resp.headers['location']:
        return True
    return False

def list_course():
    r = s.get('http://www.learning.gov.cn/study')
    r.encoding = 'utf-8'
    m = re.findall(r'course.php\?act=detail&courseid=\d+', r.text)
    courses = [re.search(r'\d+', x).group() for x in m]
    print("course list: " + str(courses))
    return courses
    
def start_course():
    login()
    delay = 1200000
    for course_id in list_course():
        set_course_session(course_id, delay)
        msg1 = log_course(course_id)
        log_id = msg1['logId']
        err = '0'
        while err != '1' :
            msg = update_time(course_id, log_id)
            err = msg['err']
            if err == '2':
                print("重新登录...")
                while login() == False:
                    time.sleep(2)
                set_course_session(course_id, delay)
                log_id = log_course(course_id)['logId']
            elif err == '0':
                time.sleep(60)
        print("完成学习： course " + course_id)            
    
def set_course_session(course_id, delay):
    data = {'act':'set_course_session', 'courseId':course_id, 'delay':delay}
    r = s.post(ajax_url, data)
    msg = json.loads(r.text)
    print(msg)
    return msg
    
def log_course(course_id):
    data = {'act':'insert', 'courseId':course_id}
    print('开始课程学习日志： course ' + course_id)
    r = s.post(ajax_url, data)
    msg = json.loads(r.text)
    print(msg)
    return msg

def update_time(course_id, log_id):
    err = 0
    msg = ''
    while err==0:
        data = {'act':'update', 'courseId':course_id, 'logId':log_id}
        r = s.post(ajax_url, data)
        msg = json.loads(r.text)
        print(msg)
        err = msg['err']
    return msg
    
    
def exit_course(course_id, log_id):
    data = {'act':'exit', 'courseId':course_id, 'logId':log_id}
    r = s.post(ajax_url, data)
    msg = json.loads(r.text)
    print(msg)
    delta = msg['playTime'] if 'playTime' in msg else 0
    total_time = str(datetime.timedelta(seconds=delta))
    print('本次共学习： '+total_time)
    
r = s.get(index_url)

r=s.get(akey_url)
data_stream = io.BytesIO(r.content)
pil_image = PIL.Image.open(data_stream)
prep_headers = {}
for s1 in headers_str.splitlines():
    s2=s1.split(': ')
    prep_headers[s2[0]]=s2[1]

