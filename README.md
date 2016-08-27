## Project：百度文库自动签到

### By:stillkam

### Program Language:python

2015.11.29


- 使用方法：

  - 安装python
  - 运行baiduwenku_PJ.py

- 实现方法

  - Tkinter实现登录界面baiduwk_gui.login()，获取用户ID和password
  - 调用baiduwk_signin.login()进行登录
    - 定制header，访问<http://www.baidu.com/cache/user/html/login-1.2.html>获取cookie及token
    - 提交用户名判断是否需要验证码，如果需要则通过codestring获取验证码图片，生成验证码填写界面输入vverifycode
    - 定制data表单，post数据给<https://passport.baidu.com/v2/api/?login>,根据reponse判断是否登录成功，如果登录成功则将用户信息写入*source/login.text*,失败则返回错误
  - 调用baiduwk_gui.status()显示登陆状态
    - 使用python threading 库新建子线程执行baiduwk_signin.trysigin()实现签到
      - 读取*source/log.text*获取签到信息，若已签到则睡眠6h；若未签到则每隔0.5h尝试签到，成功则睡眠6h
      - 签到方法：定制header,连同登录得到的cookie一起get到<http://wenku.baidu.com/task/submit/signin>，根据reponse判断是否签到成功
      - 重复以上过程，实现自动签到
    - 读取*source/log.text*日志获取登录状态并在界面上显示
    - 点击*update status*按钮刷新签到状态
    - 点击*switch account*登录新账户
