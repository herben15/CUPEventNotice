# 中石大第二课堂活动通知

## 项目地址

https://github.com/herben15/CUPEventNotice



## 项目背景

本人深受第二课堂没有通知而导致很多活动没有报上，因此创建了这个项目



## 项目环境

可以使用Windows，ubantu等，python使用python3



## 项目依赖

本项目依赖的外部包有`requests`、`schedule`、`yagmail`；使用以下命令可安装好这些包

````pip
pip install requests
pip install schedule
pip install yagmail
````



## 项目准备

### 修改邮件

在`send_mes.py`文件中修改邮件，具体是`send_username`修改为你自身的邮件账号，`receiver_1`修改为接收信息的邮件账号，`authorization`为授权码，具体看下面。

#### 获取authorization

本操作以qq邮箱为例，其他邮箱请自行查阅。

登录qq邮箱【本人用网页版】——> 设置 ——> 账号 ——> POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务 ——> 根据提示开启服务并获取`authorization`值即可

### 修改请求头和cookies

请访问网页（[点我](https://sct.cup.edu.cn/activitynew/mobile/activity/list)），若需要登录则先登录（登录后再访问）——> 右击检查（或者F12）——> 点击网络 ——> 点击网页中的德育 ——> 点击检查中的list ——> 点击标头 ——> 找到请求标头下的**User-Agent**（需要复制）——> 点击上方的**Cookies** —— > 下方有两个值

根据上面的结果，修改`fecth.py`中的全局变量`headers`和`cookies`，headers中的User-Agent需要修改为你的值，Cookies中的两个值对应修改为你的值



## 项目测试

若是用pycharm则直接运行`test.py`文件，根据输出结果判断是否能够正确运行。

若是用命令行，则先进入src目录中,然后运行test.py文件

```
cd src
python3 test.py
```

同样根据输出结果判断是否正确运行



## 项目上线

这个项目需要使用服务器的。但有些点需要注意。

不能直接使用命令`python3 fecth.py &`运行，因为关闭控制台后会杀死程序。需要执行以下命令

```
nohup python3 fecth.py &
```

当输出`nohup: ignoring input and appending output to 'nohup.out'`就表示成功了，接下来就等消息即可。



## 接收处理

当邮件接收到程序异常错误时，一般是你的cookies更新了，需要你手动更新后再次运行程序。【目前不知道刷新时间，若刷新时间过快，我会考虑自动更新cookies】

## 个人博客

[herben' blog](http://herben.top/)
