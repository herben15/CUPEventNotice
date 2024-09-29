# -*- coding: utf-8 -*-

import os.path
import requests
import schedule
import time
import random
import send_mes
from datetime import datetime
import sys
import get_cookies

# 用于存储活动名称的集合
existing_activities_id = set()
# 用于更新存储数据
new_activities_id = set()

headers = {
    'User-Agent': '',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'https://sct.cup.edu.cn/activitynew/mobile/activity/list',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://sct.cup.edu.cn',
    'Connection': 'keep-alive'
}

cookies = {
    'UM_distinctid': '',
    'PHPSESSID': ''
}

URL = 'https://sct.cup.edu.cn/activitynew/mobile/activity/list'

classification = [13, 26, 14, 15, 16, 23, 24, 17, 25, 22, 21, 20]
classification_title = {
    '13': '（德育）思想引领',
    '26': '（德育）党团班主题教育',
    '14': '（德育）形势政策',
    '16': '（体育）体育类',
    '23': '（体育）体育类主题讲座',
    '24': '（美育）文化艺术类主题讲座',
    '17': '（美育）美育熏陶',
    '25': '（美育）文化活动',
    '22': '（劳育）院级劳动实践',
    '21': '（劳育）生产劳动实践',
    '20': '（劳育）校园劳动实践'
}


def log(message):
    now = datetime.now()
    with open('log.txt', 'a', encoding='utf-8') as file:
        file.write(f"{now}: \n{message}\n")


def fetch_activities():
    session = requests.Session()
    activities = []
    cnt = 0

    for cls in classification:
        data = {'classificationid': cls, 'random': random.random()}  # 根据实际参数调整

        try:
            response = session.post(URL, headers=headers, cookies=cookies, data=data)
            response.raise_for_status()  # 检查请求是否成功

            if response.ok:
                json_data = response.json()
                if 'data' in json_data and 'compList' in json_data['data']:
                    for item in json_data['data']['compList']:
                        if item['id'] not in existing_activities_id:
                            new_activity = {'title': item['title'], 'classificationtitle': item['classificationtitle']}
                            activities.append(new_activity)
                            existing_activities_id.add(item['id'])
                else:
                    log("返回数据中没有活动列表")
                    return False  # 返回False表示未找到活动

            else:
                log(f"请求失败，状态码: {response.status_code}")
                return False

        except requests.exceptions.RequestException as e:
            log(f"请求发生错误: {e}"+" 可能是cookie错误")
            return False
        except ValueError:
            log("返回的数据不是有效的JSON格式")
            return False

        time.sleep(2)  # 控制请求频率
        cnt += 1
        print(f"完成 {cnt * 100 / len(classification):.2f}%...")

    log_content = "\n".join(f"类型：{item['classificationtitle']}\t标题：{item['title']}" for item in activities)
    if not log_content:
        log_content = "无新活动"

    log("新活动日志：\n"+log_content)

    if activities:  # 如果有新活动，发送消息
        send_mes.send([f"类型：{item['classificationtitle']} 标题：{item['title']}" for item in activities])

    return True  # 返回True表示成功

def send_error(content):
    send_mes.send(content)

def init():
    now = datetime.now()
    if not os.path.exists('log.txt'):
        with open('log.txt', 'w', encoding='utf-8') as file:
            file.write(f"内容：日志\n创建时间：{now}\n")
    if not os.path.exists('activites.txt'):
        with open('activites.txt','w',encoding='utf-8') as file:
            file.write(f"内容：活动列表\n创建世界：{now}\n")
    else:
        with open('activites.txt','r',encoding='utf-8') as file:
            lines = file.readlines()
            if len(lines) >= 3:  # 确保有足够的行
                integer_line = lines[2].strip()  # 获取第三行的整数数据
                integers = map(int, integer_line.split())  # 将字符串分割并转换为整数
                existing_activities_id.update(integers)  # 将整数添加到集合中
    P=get_cookies.get_cookies()
    if P:
        cookies["PHPSESSID"]=P
        print(f"新获取的cookie是:{P}")
    else:
        log("cookie获取错误")
        send_error(["cookie获取错误，请尽快检查程序"])
        sys.exit()


def updata_activites():
    with open('activites.txt','a',encoding='utf-8') as file:
        for item in new_activities_id:
            file.write(f' {item}')


def job():
    reslut=fetch_activities()
    if not reslut:  #获取失败，强制退出程序
        #尝试获取新cookie
        res=get_cookies.get_cookies()
        if res:
            cookies['PHPSESSID']=res
            #检查是否可以了
            if not fetch_activities():
                # 不是cookie错误，其余问题
                log("异常退出")
                send_error(["异常退出，请检查日志文件解决问题"])
                updata_activites()  # 更新数据，以便下次启动重复发送数据
                sys.exit()
        else:
            log("cookie获取错误")
            send_error(["cookie获取错误，请尽快检查程序"])
            updata_activites()  # 更新数据，以便下次启动重复发送数据
            sys.exit()

# 启动爬虫
if __name__ == '__main__':
    init()  # 初始化
    cnt=1
    limit=168   #7天退出一次

    # 定时任务设置
    schedule.every(2).hours.do(job)  # 每2个小时执行一次

    while cnt<=limit:
        schedule.run_pending()
        time.sleep(3600)
        cnt+=1
        if cnt<=20: # 前5次测试程序运行效果
            send_mes.send([f'程序测试中，第{cnt}次'])
        print("检查...")
    log("正常退出")
    send_error(["正常执行结束，若有需要请自行重新启动"])
    updata_activites()  # 更新数据，以便下次启动重复发送数据
