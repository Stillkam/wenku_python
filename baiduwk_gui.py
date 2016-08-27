# -- coding: utf-8 --
# author:13307130342xiangjie

from Tkinter import *
import time,threading
import baiduwk_signin

def login():
    def lgi():
        Bid=entry1.get()
        Bps=entry2.get()
        err=baiduwk_signin.login(Bid,Bps)

        if err=='0':
            me.set('1'+Bid)
            root.destroy()
            status(Bid)
        elif err=='7':
            me.set('Your PASSWORD is Wrong!')

        elif err=='257':
            me.set('Your Verifycode is Wrong!')
        elif err=='1':
            me.set('Your ID is Wrong!')
        else:
            me.set('Some Problem Happened...')
    root=Tk(className='百度文库自动签到')
    root.iconbitmap('source/social_round_blogger_128px_1196623_easyicon.net.ico')
    me=StringVar()
    me.set('BAIDU LOGIN')
    mes=Label(root,textvariable=me)
    mes.grid(row=0,column=1,columnspan=2,pady=10)
    baiduid=Label(root,text='    BAIDU    ID    ')
    baiduid.grid(row=1)
    entry1=Entry(root,bd=2)
    entry1.grid(row=1, column=1,pady=20,padx=30)
    password=Label(root,text='    PASSWORD    ')
    password.grid(row=2)
    entry2=Entry(root,bd=2)
    entry2.grid(row=2, column=1,pady=10)
    entry2['show'] = '*'
    bs=Button(root,text='       LOGIN      ',bg='grey',command=lgi)
    bs.grid(row=3,column=1,columnspan=2,pady=10,padx=30)
    root.mainloop()
    if me.get()[0]=='1':
        return me.get()[1:]
    else:
        return 0

def status(baiduID):
    thread1=threading.Thread(target=trysigin,args=(baiduID,))
    thread1.start()
    date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    log=getstatus()
    status=''
    if log=='':
        status='false'
    else:
        logifo=eval(log)
        if logifo['baiduID']==baiduID and logifo['date']==date and logifo['status']=='true':
            status='true'
        else:
            status='false'
    def switch():
        delet=open('source/login.text','w')
        delet.close()
        root.destroy()
        login()
    def update():
        date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        datenow.set(date)
        logifo=eval(getstatus())
        if logifo['baiduID']==baiduID and logifo['date']==date and logifo['status']=='true':
            status='true'
        else:
            status='false'
        statusnow.set(status)
    root=Tk(className='百度文库自动签到')
    root.iconbitmap('source/social_round_blogger_128px_1196623_easyicon.net.ico')
    label1=Label(root,text='BaiduID:')
    label1.grid(row=0,column=0,pady=10,padx=30,sticky='e')
    baiduid=Label(root,text=baiduID)
    baiduid.grid(row=0,column=1,pady=10,padx=30,sticky='w')
    label2=Label(root,text='DATE:')
    label2.grid(row=1,column=0,pady=10,padx=30,sticky='e')
    datenow=StringVar()
    datenow.set(date)
    datelabel=Label(root,textvariable=datenow)
    datelabel.grid(row=1,column=1,pady=10,padx=30,sticky='w')
    label3=Label(root,text='STATUS:')
    label3.grid(row=2,column=0,pady=10,padx=30,sticky='e')
    statusnow=StringVar()
    statusnow.set(status)
    statuslabel=Label(root,textvariable=statusnow)
    statuslabel.grid(row=2,column=1,pady=10,padx=30,sticky='w')
    bt1=Button(root,text='Switch Account',bg='grey',command=switch)
    bt1.grid(row=3,column=0,pady=10,padx=30)
    bt2=Button(root,text='Update Status',bg='grey',command=update)
    bt2.grid(row=3,column=1,pady=10,padx=30)
    root.mainloop()

def trysigin(baiduID):
    date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    logifo=eval(getstatus())
    if logifo['baiduID']==baiduID and logifo['date']==date and logifo['status']=='true':
        time.sleep(60*60*6)
    else:
        while 1:
            sgi=baiduwk_signin.signin()
            if sgi=='0':
                log={}
                log['baiduID']=eval(open('source/login.text','r').read())['baiduID']
                log['date']=date
                log['status']='true'
                open('source/log.text','a').write(str(log)+'\n')
                break
            else:
                time.sleep(60*30)

def getstatus():
    logfile=open('source/log.text','a+')
    log=logfile.readlines()
    logfile.close()
    return log[-1]

#login()
