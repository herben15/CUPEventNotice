# -*- coding: utf-8 -*-

import sys
import fecth
import schedule
import time

if __name__=='__main__':
    fecth.init()
    print("测试是否正常获取数据")
    if fecth.fetch_activities():
        print("获取数据正常，请检查是否获取到邮件")
        mes=input("获取输入1，为获取输入0：")
        if mes=="0":
            print("请检查你的邮件是否填写正确")
            sys.exit()
    else:
        print("数据获取异常，请检查日志文件并解决问题")
        sys.exit()

    print("测试程序能否完整运行")
    cnt = 1
    limit = 15
    schedule.every(5).seconds.do(fecth.job)
    while cnt <= limit:
        schedule.run_pending()
        time.sleep(1)
        cnt+=1
        print("检查...")
    fecth.log("正常退出")
    print("测试完成")

    print("测试是否能够正常地异常退出")
    fecth.cookies['PHPSESSID']=''
    if not fecth.fetch_activities():
        print("正常")
    else:
        print("程序异常，请修改程序")
        sys.exit()

    print("测试异常退出时能否及时通知，请查看邮箱")
    cnt = 1
    limit = 15
    schedule.every(5).seconds.do(fecth.job)
    while cnt <= limit:
        schedule.run_pending()
        time.sleep(1)
        cnt+=1
        print("检查...")
    fecth.log("正常退出")
    print("异常！job函数异常，没有异常退出")