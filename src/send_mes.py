# -*- coding: utf-8 -*-
import sys

import yagmail
import smtplib  # 需要导入 smtplib

def send(content):
    send_username = ''
    receiver = ''
    authorization = ''

    subject = '第二课堂活动提醒'
    contents=""
    for item in content:
        contents+=item+"\n"
    try:
        yag = yagmail.SMTP(user=send_username, password=authorization, host='smtp.qq.com')
        yag.send(to=receiver, subject=subject, contents=content)
    except smtplib.SMTPServerDisconnected as e:
        send_username='备用账号'
        receiver_1=''
        authorization=''
        yag = yagmail.SMTP(user=send_username, password=authorization, host='smtp.qq.com')
        yag.send(to=receiver_1, subject=subject, contents="邮箱发送错误，可能是封数限制")
        sys.exit()

if __name__ == '__main__':
    content=['测试','第一行','第二行']
    send(content)
