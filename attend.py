#!/usr/bin/env python3
"""
Created on Sat Nov 21 13:07:56 2015

@author: xiaohu
"""
import sys
import requests
import json
import logging
import logging.handlers
import time
import numpy

LOG_FILE = 'sign/sign.log'  
  
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)  
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'  
  
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)      
  
logger = logging.getLogger('sign')    
logger.handlers = []
logger.addHandler(handler)           
logger.setLevel(logging.DEBUG)  

s= requests.Session()
s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'
s.headers['Accept']='application/json, text/javascript, */*; q=0.01'
s.headers['Accept-Language']='zh-CN,zh;q=0.8'
s.headers['Referer']='http://10.32.127.151/index/index/index.html'
login_url = "http://10.32.127.151/Home/Login/login_submit"
sign_url = "http://10.32.127.151/index/index/sign/P/"
logout_url = "http://10.32.127.151/Home/Login/logout"
logname = '339005198609279316'
passwd = '123456'
repeat_times = 3
sleep_time = 2


def login():
    data = {'logname':logname, 'passwd':passwd}
    resp = s.post(login_url, data, allow_redirects=False)
    print(s.headers)
    resp.encoding = 'utf-8'
    print(resp.status_code)
    print(resp.headers)
    print(resp.text)
    if '/index/index/index.html' in resp.headers['location']:
        logger.info(logname + " login success!")
        return True
    logger.info(logname + " login failed!")
    print('Login Error!')
    return False
    
def sign(act):
    logger.info(logname + " start sign "+act)
    r = s.get(sign_url+act)
    print(s.headers)
    r.encoding = 'utf-8-sig'
    ret = json.loads(r.text)
    msg = ret['msg']
    logger.info(logname + ' ' + msg)
    print(msg)
    if(ret['result'] == 'scuuess'):
        return True
    return 
    
def logout():
    s.get(logout_url)
    print(s.headers)
    logger.info(logname + " logout!")



    
if __name__ == '__main__':
    if(len(sys.argv) > 1 and sys.argv[1] in ['in','out']):
        act = sys.argv[1]
        time.sleep(numpy.random.randint(5*60))
        with open('sign/id.txt', 'r') as f:
            for l in f.readlines():
                logname = l.strip()
                logger.info('---------------------start sign procedure for: ' + logname + '---------------------')
                for j in range(repeat_times):
                    try:
                        login()
                        sign(act)
                        logout()
                        break
                    except Exception as ex:
                        logger.error(ex)
                        logger.info('retry: '+str(j))
                        if(j == repeat_times - 1):
                            sys.exit(1)
                        time.sleep(sleep_time*(60 if j==repeat_times-2 else j))
                time.sleep(numpy.random.randint(60))
                
        sys.exit(0)
    else: 
        print("choose your act from in and out.")
        sys.exit(2)           
