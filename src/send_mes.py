# -*- coding: utf-8 -*-

import yagmail

def send(content):
    send_username = 'your_email'
    receiver_1 = 'recevier_email'
    authorization = ''

    subject = '第二课堂活动提醒'
    contents=""
    for item in content:
        contents+=item+"\n"
    yag = yagmail.SMTP(user=send_username, password=authorization, host='smtp.qq.com')
    yag.send(to=receiver_1, subject=subject, contents=content)

if __name__ == '__main__':
    content=['测试','第一行','第二行']
    send(content)