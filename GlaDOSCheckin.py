# -*- coding: utf-8 -*-
"""
cron: 0 30 8 * * ?
new Env('GlaDOS签到');
"""
import json
import requests
from datetime import datetime
import os
import sys
import re

## 获取通知服务
class msg(object):
    def __init__(self, m):
        self.str_msg = m
        self.message()
    def message(self):
        global msg_info
        print(self.str_msg)
        try:
            msg_info = "{}\n{}".format(msg_info, self.str_msg)
        except:
            msg_info = "{}".format(self.str_msg)
        sys.stdout.flush()
    def getsendNotify(self, a=0):
        if a == 0:
            a += 1
        try:
            url = 'https://gitee.com/curtinlv/Public/raw/master/sendNotify.py'
            response = requests.get(url)
            if 'curtinlv' in response.text:
                with open('sendNotify.py', "w+", encoding="utf-8") as f:
                    f.write(response.text)
            else:
                if a < 5:
                    a += 1
                    return self.getsendNotify(a)
                else:
                    pass
        except:
            if a < 5:
                a += 1
                return self.getsendNotify(a)
            else:
                pass
    def main(self):
        global send
        cur_path = os.path.abspath(os.path.dirname(__file__))
        sys.path.append(cur_path)
        if os.path.exists(cur_path + "/sendNotify.py"):
            try:
                from sendNotify import send
            except:
                self.getsendNotify()
                try:
                    from sendNotify import send
                except:
                    print("加载通知服务失败~")
        else:
            self.getsendNotify()
            try:
                from sendNotify import send
            except:
                print("加载通知服务失败~")
        ###################
msg("").main()


#获取变量token，userid
def get_cookie():
    cookies = []
    url='http://127.0.0.1:5600/api/envs'
    with open('/ql/config/auth.json', 'r') as f:
        token=json.loads(f.read())['token']
    headers={
        'Accept':'application/json',
        'authorization':'Bearer '+token,
        }
    response=requests.get(url=url,headers=headers)
    for i in range(len(json.loads(response.text)['data'])):
        if json.loads(response.text)['data'][i]['name'] =='GlACK':
            try:
                env = re.split("&|,|，|\\s",json.loads(response.text)['data'][i]['value'])
                for item in env:
                    if item == '':
                        pass
                    else:
                        cookies.append(item)
            except:
                pass
    return cookies

def get_info(cookie):
    msg = []
    url = 'https://glados.rocks/api/user/status'
    headers ={
        'Host': 'glados.rocks',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'Cookie':cookie,
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1',
        'Authorization': '1771266723009394620993268546288-844-390',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
             }
    #获取账户信息
    response = requests.get(url = url, headers=headers)
    result = json.loads(response.text)
    print("正在获取账户信息……")
    try:
        if result['code'] == 0:
            print(f"当前账号：{result['data']['email']} ，剩余天数：{float(result['data']['leftDays'])}天")
            msg.append(result['data']['email'] +" , 剩余天数：" + str(float(result['data']['leftDays'])))
        else:
            print("cookie失效")
            msg.append("cookie失效")
    except:
        print("未知错误，检查cookie格式")
    return msg

def task(cookie):
    msg = []
    url = 'https://glados.rocks/api/user/checkin'
    headers ={
        'Host': 'glados.rocks',
        'Content-Type': 'application/json;charset=utf-8',
        'Origin': 'https://glados.rocks',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': cookie,
        'Connection':'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1',
        'Authorization': '1771266723009394620993268546288 - 844 - 390',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
             }
    #签到任务
    response = requests.post(url=url, headers=headers,data=json.dumps({'token': 'glados.network'}))
    result = json.loads(response.text)
    try:
        if result['code'] == 0:
            print(f"{result['message']} ，剩余天数：{float(result['list']['balance'])}天")
            msg.append(result['message']+ " ，剩余天数："+str(float(result['list']['balance'])))
        else:
            print(f"{result['message']},省省吧，别鸡儿一直签了")
            msg.append(result['message']+",省省吧，别鸡儿一直签了")
    except:
        print("未知错误，检查cookie格式")
    return msg

if __name__ == '__main__':
    msg = ''
    cookies = get_cookie()[0]
    for ck in cookies:
        msg += get_info(ck)
        msg += task(ck)
    msg += "\n"+"时间："+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    send("GlaDos签到通知",msg)

