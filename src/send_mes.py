import yagmail
import smtplib

def send(content,subject = '第二课堂活动提醒'):
    send_username = ''
    receiver_1 = ''
    authorization = ''

    contents=""
    if type(content)==str:
        contents=content
    else:
        for item in content:
            contents+=item+"\n"

    try:
        yag = yagmail.SMTP(user=send_username, password=authorization, host='smtp.qq.com')
        yag.send(to=receiver_1, subject=subject, contents=contents)
    except smtplib.SMTPServerDisconnected as e:
        send_username=''
        receiver_1=''
        authorization=''
        yag = yagmail.SMTP(user=send_username, password=authorization, host='smtp.qq.com')
        yag.send(to=receiver_1, subject=subject, contents="邮箱发送错误，可能是封数限制")

if __name__ == '__main__':
    # content=['测试','第一行','第二行']
    # send(content)
    send("字符串测试")