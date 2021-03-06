# coding=utf-8

import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
'''
---单线程---
init() 用于模拟登陆
加密方式：BASE64
'''

from outnetUtil import OutNetLink
import time
import datetime
import re

prefix = 'https://ssl.hrbeu.edu.cn/web/1/http/1/'


def https_url(url):
    return prefix + url[7:]


def init():
    # 登录
    global prefix
    s = OutNetLink.getConn()
    url = 'http://edusys.hrbeu.edu.cn/jsxsd/xk/LoginToXk'
    url = https_url(url)
    data = {
        'encoded': 'MjAxNTIwMTEwOA==%%%and0MTk5ODAzMzE='
    }
    cur = s.post(url=url, data=data)
    # print(cur.text)
    # print(s.cookies)

    # 点击选课中心
    url = 'http://edusys.hrbeu.edu.cn/jsxsd/xsxk/xklc_list.do?Ves632DSdyV=NEW_XSD_PYGL'
    url = https_url(url)
    cur = s.get(url)
    # print(cur.text)
    # print(s.cookies)

    # 进入选课按钮 第一次
    url = 'http://edusys.hrbeu.edu.cn/jsxsd/xsxk/xklc_view.do?jx0502zbid=5868B0BE07B04121BECFAF0F50DDD02C'
    url = https_url(url)
    cur = s.get(url)
    # print(cur.text)
    # print(s.cookies)

    #进入选课按钮 第二次
    url = 'http://edusys.hrbeu.edu.cn/jsxsd/xsxk/xsxk_index.do?jx0502zbid=5868B0BE07B04121BECFAF0F50DDD02C'
    url = https_url(url)
    cur = s.get(url)
    curtext = cur.text
    # print(cur.text)
    # print(s.cookies)
    patten = '当前未开放选课'
    cntt = 0
    while 1:
        cur = s.get(url)
        curtext = cur.text
        ret = re.search(pattern=patten, string=curtext)
        if ret is None:
            break
        time.sleep(1)
        cntt += 1
        print('the system is close, trying to login', cntt)
    return s


def thread_make(url, name, s):
    global finish
    if finish.get(name):
        return 0
    else:
        # th = threading.Thread(target=get_lesson, args=(url,name,s))
        th = get_lesson(url, name, s)
        if th == -1:
            return -1
        elif th == 3:
            return 3
    return 0


def get_lesson(url, name, s):
    global finish, times
    if times.get(name) is None:
        times[name] = 0
    try:
        ans = s.get(url)
        ret = ans.json()
        # print(ret)
        times[name] += 1
        if ret['success']:
            print(name, '第', times[name], '次抢课尝试成功  信息：%r 时间：' % (ret['message']), datetime.datetime.now())
            return 1
        elif '选课失败：此课程已选！' in ret['message']:
            print(name, '第', times[name], '次抢课时发现已选 信息：%r 时间：' % (ret['message']), datetime.datetime.now())
            finish['name'] = True
            return 2
        elif '当前账号已在别处登录' in ret['message']:
            return 3
        else:
            print(name, '第', times[name], '次抢课尝试未中 信息：%r 时间：' % (ret['message']), datetime.datetime.now())
            return 0
    except:
        return -1


def login():
    while 1:
        try:
            s = init()
            print('登陆成功！ 时间：', datetime.datetime.now())
        except:
            wait = 0.1
            print('网络阻塞，%d秒后重启连接！ 时间：' % wait, datetime.datetime.now())
            time.sleep(wait)
        else:
            return s


def work(s, url_list):
    while 1:
        for url in url_list:
            res = thread_make(url[0], url[1], s)
            if res == -1 or res == 3:
                break
        time.sleep(0.01)


times = dict()
finish = dict()


def link_start():
    s = login()
    url_list = [
        (https_url('http://edusys.'
                   'hrbeu.edu.cn/jsxsd/xsxkkc/xxxkO'
                   'per?jx0404id=201720182004114'), '软件项目管理'),

    ]
    work(s, url_list)


if __name__ == '__main__':
    link_start()

'''
def get1():
    cnt = 1
    while (1):
        ans = s.get('http://edusys.hrbeu.edu.cn/jsxsd/xsxkkc/xxxkOper?jx0404id=201720181004724')
        ret = ans.json()
        print(ret)
        if (ret['success'] == True):
            break
        else:
            time.sleep(0.2)
            print('系统设计', cnt)
            cnt += 1

def get2():
    cnt = 1
    while (1):
        ans = s.get('http://edusys.hrbeu.edu.cn/jsxsd/xsxkkc/xxxkOper?jx0404id=201720181004689')
        ret = ans.json()
        print(ret)
        if (ret['success'] == True):
            break
        else:
            time.sleep(0.2)
            print('信息安全', cnt)
            cnt += 1

def get3():
    cnt = 1
    while (1):
        ans = s.get('http://edusys.hrbeu.edu.cn/jsxsd/xsxkkc/xxxkOper?jx0404id=201720181004699')
        ret = ans.json()
        print(ret)
        if (ret['success'] == True):
            break
        else:
            time.sleep(0.2)
            print('C++', cnt)
            cnt += 1


try:
    _thread.start_new_thread(get1, ())
    _thread.start_new_thread(get2, ())
    _thread.start_new_thread(get3, ())
except:
    print("wrong")

while(1):
    pass



'''
