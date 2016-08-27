# -- coding:utf-8 --
# author:13307130342xiangjie

import urllib, urllib2, cookielib, re, time
import requests


def login(baiduID,password):
    headers = {
        "Host":"passport.baidu.com",
        "Referer":"http://www.baidu.com/cache/user/html/login-1.2.html",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36",
        "Origin":"http://www.baidu.com",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Cache-Control":"max-age=0",
        "Connection":"keep-alive"
        }
    cookie = cookielib.MozillaCookieJar('source/--login-baidu--')
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

    loginUrl = 'http://www.baidu.com/cache/user/html/login-1.2.html'
    getTokenUrl = 'https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=true'
    getCodeStringUrl = 'https://passport.baidu.com/v2/api/?logincheck&callback=bdPass.api.login._needCodestringCheckCallback&tpl=mn&charset=UTF-8&index=0&username=' + baiduID + '&isphone=false&time=1436429688644'
    loginPostUrl = 'https://passport.baidu.com/v2/api/?login'

    request = urllib2.Request(loginUrl, headers=headers)
    response = opener.open(request)

    request = urllib2.Request(getTokenUrl, headers=headers)
    response = opener.open(request)
    hasToken= response.read()
    token = re.search(r'login_token=\'(.+?)\'',hasToken).group(1)

    request = urllib2.Request(getCodeStringUrl, headers=headers)
    response = opener.open(request)
    getCodeString = response.read()
    codestring = re.search(r'"codestring":"?([^"]+)"?,', getCodeString).group(1)
    if codestring == 'null' :
        codestring = ''
        verifycode = ''
    else:
        genimageUrl = 'https://passport.baidu.com/cgi-bin/genimage?' + codestring + '&v=' + str(long(time.time()*1000))
        import io, Tkinter as tk
        from PIL import Image, ImageTk
        request = urllib2.Request(genimageUrl, headers=headers)
        image_bytes = opener.open(request).read()
        pil_image = Image.open(io.BytesIO(image_bytes))

        def presskey(event):
            global verifycode
            if event.keycode == 13:
                verifycode = entry.get()
                tk_root.destroy()

        tk_root = tk.Tk(className='百度文库自动签到')
        tk_root.iconbitmap('source/social_round_blogger_128px_1196623_easyicon.net.ico')
        tk_image = ImageTk.PhotoImage(pil_image)
        label1 = tk.Label(tk_root, text='Please input verifycode')
        label1.pack()

        label2 = tk.Label(tk_root, image=tk_image)
        label2.pack()

        entry = tk.Entry(tk_root)
        entry.bind('<Key>', presskey)
        entry.pack()
        tk_root.mainloop()

    data = {
        "ppui_logintime":"134198",
        "charset":"utf-8",
        "codestring":"",
        "index":"0",
        "u":"",
        "safeflg":"0",
        "staticpage":"http://www.baidu.com/",
        "loginType":"1",
        "tpl":"mn",
        "callback":"parent.bdPass.api.login._postCallback",
        "mem_pass":"on"
        }
    data['token'] = token
    data['username'] = baiduID
    data['password'] = password
    data['codestring'] = codestring
    data['verifycode'] = verifycode
    if '@' in baiduID:
        data['isPhone']='false'
    else:
        data['isPhone']='true'

    r = urllib2.Request(loginPostUrl, urllib.urlencode(data), headers)
    result = opener.open(r).read()
    errno = re.search(r'&error=(\d+)', result).group(1)
    if errno == '0':
        cookie.save(ignore_discard=True,ignore_expires=True)
        log={}
        log['baiduID']=baiduID
        log['password']=password
        loginlog=open('source/login.text','w')
        loginlog.write(str(log))
    return errno


def signin():
    headers = {
        "Host":"wenku.baidu.com",
        "Referer":"http://wenku.baidu.com/task/browse/daily",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36",
        "Accept":"*/*",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
        "Connection":"keep-alive",
        "X-Requested-With": "XMLHttpRequest"
        }
    cookie = cookielib.MozillaCookieJar('source/--login-baidu--')
    cookie.load('source/--login-baidu--', ignore_discard=True, ignore_expires=True)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    signinurl='http://wenku.baidu.com/task/submit/signin'
    request = urllib2.Request(signinurl, headers=headers)
    response = opener.open(request)
    text= response.read()
    return eval(text)['errno']
