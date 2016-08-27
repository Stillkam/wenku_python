# -- coding: utf-8 --
# author:13307130342xiangjie

import baiduwk_gui

baiduID=''
password=''
login=open('source/login.text','a+')
loginifo=login.read()
if loginifo=='':
    baiduID=baiduwk_gui.login()
else:
    lgifo=eval(loginifo)
    baiduID=lgifo['baiduID']
    password=lgifo['password']
login.close()
if baiduID!=0:
    baiduwk_gui.status(baiduID)
