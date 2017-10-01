# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 11:52:26 2016

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
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,QLineEdit,QPushButton

class Example(QWidget):
    s = requests.Session()
    root_url = "http://www.learning.gov.cn"
    login_url = "http://www.learning.gov.cn/study/login.php"
    ajax_url = "http://www.learning.gov.cn/study/ajax.php"
    course_url = "http://www.learning.gov.cn/course/course.php"
    index_url = root_url + "/index.php"
    akey_url = root_url + "/system/akey_img.php"
    post_data="act=AjaxLogin&username=330121196308266325&password=08266325&islogin=0&authKey="
    
    headers_str = """Connection: close
Accept: application/json, text/javascript, */*; q=0.01
Origin: http://www.learning.gov.cn
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Referer: http://www.learning.gov.cn/index.php
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.8"""

    html_header = """Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36
Referer: http://www.learning.gov.cn/study/
Accept-Encoding: gzip, deflate, sdch
Accept-Language: zh-CN,zh;q=0.8"""

    def __init__(self):
        super().__init__()
        
        self.r = self.s.get(self.index_url)

        self.r=self.s.get(self.akey_url)
        data_stream = io.BytesIO(self.r.content)
        pil_image = PIL.Image.open(data_stream)
        prep_headers = {}
        for s1 in self.headers_str.splitlines():
            s2=s1.split(': ')
            prep_headers[s2[0]]=s2[1]
        self.s.headers.update(prep_headers)
        self.initUI()

        
    def initUI(self):

        self.pic = QtGui.QPixmap()
        self.label = QLabel()
        self.pic.loadFromData(QtCore.QByteArray(self.r.content))
        self.label.setPixmap(self.pic)

        self.lineedit = QLineEdit()
        self.pushbtn = QPushButton("提交")
        self.hbox = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.pushbtn)
        self.hbox.addWidget(self.label)
        self.hbox.addWidget(self.lineedit)
        self.pushbtn.clicked.connect(self.buttonClicked)
        
        self.move(300, 200)
        self.setWindowTitle('Red Rock')
        self.show()

    def buttonClicked(self):

        self.start_course()

    def login(self):
        self.r = self.s.post(self.login_url, self.post_data + self.lineedit.text(), allow_redirects=False)
        print("login post: ")
        print(self.r)
        print(self.r.text)


    def list_course(self):
        #self.update_headers(self.html_header)
        r = self.s.get('http://www.learning.gov.cn/study')
        r.encoding = 'utf-8'
        print(r.text)
        m = re.findall(r'course.php\?act=detail&courseid=\d+', r.text)
        courses = [re.search(r'\d+', x).group() for x in m]
        print("course list: " + str(courses))
        return courses

    def update_headers(self, header_string):
        prep_headers = {}
        for s1 in header_string.splitlines():
            s2 = s1.split(': ')
            prep_headers[s2[0]] = s2[1]
        self.s.headers.update(prep_headers)

    def start_course(self):
        self.login()
        delay = 1200000
        for course_id in self.list_course():
            self.set_course_session(course_id, delay)
            msg1 = self.log_course(course_id)
            log_id = msg1['logId']
            err = '0'
            while err != '1':
                msg = self.update_time(course_id, log_id)
                err = msg['err']
                if err == '2':
                    print("重新登录...")
                    while self.login() == False:
                        time.sleep(2)
                    self.set_course_session(course_id, delay)
                    log_id = self.log_course(course_id)['logId']
                elif err == '0':
                    time.sleep(60)
            print("完成学习： course " + course_id)

    def set_course_session(self, course_id, delay):
        data = {'act': 'set_course_session', 'courseId': course_id, 'delay': delay}
        r = self.s.post(self.ajax_url, data)
        msg = json.loads(r.text)
        print(msg)
        return msg

    def log_course(self, course_id):
        data = {'act': 'insert', 'courseId': course_id}
        print('开始课程学习日志： course ' + course_id)
        r = self.s.post(self.ajax_url, data)
        msg = json.loads(r.text)
        print(msg)
        return msg

    def update_time(self, course_id, log_id):
        err = 0
        msg = ''
        while err == 0:
            data = {'act': 'update', 'courseId': course_id, 'logId': log_id}
            r = self.s.post(self.ajax_url, data)
            msg = json.loads(r.text)
            print(msg)
            err = msg['err']
        return msg

    def exit_course(self, course_id, log_id):
        data = {'act': 'exit', 'courseId': course_id, 'logId': log_id}
        r = self.s.post(self.ajax_url, data)
        msg = json.loads(r.text)
        print(msg)
        delta = msg['playTime'] if 'playTime' in msg else 0
        total_time = str(datetime.timedelta(seconds=delta))
        print('本次共学习： ' + total_time)


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
