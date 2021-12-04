#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import datetime
import time
import re

import requests


# 获取当前时间+8小时时差
def now():
    now1 = datetime.datetime.now()
    now1 += datetime.timedelta(hours=8)
    rightnowcn = now1.strftime('%Y/%m/%d %I:%M %p')
    return rightnowcn


# 获取当前时间+8小时时差的时间戳
def nowstamp():
    dtime = datetime.datetime.now()
    dtime += datetime.timedelta(hours=8)
    timestamp = int(time.mktime(dtime.timetuple()))
    return timestamp


# cookie字符串解析成字典
def cookieParse(cookiesStr):
    cookie_dict = {}
    cookies = cookiesStr.split(';')

    for cookie in cookies:
        cookie = cookie.split('=')
        cookie_dict[cookie[0]] = cookie[1]

    return cookie_dict


def cookieParseV2ex(cookieStr):
    cookie_dist = {}
    cookies = cookieStr.split(';')
    for cookie in cookies:
        if cookie.find('"') > 0:
            cookie = cookie.split('="')
            cookie_dist[cookie[0]] = cookie[1].replace('"', '')
        else:
            cookie = cookie.split('=')
            cookie_dist[cookie[0]] = cookie[1]

    return cookie_dist


# 使用Qmsg酱发送推送信息
def sendQmsgInfo(msg):
    url = 'https://qmsg.zendee.cn/send/'
    url += os.environ["QMSGAPI"]
    data = {'msg': msg}
    requests.post(url, data)


def send_telegram(msg):
    url = 'https://api.telegram.org/bot'
    url += os.environ["TGAPI"]
    url += '/sendMessage'
    data = {'chat_id': os.environ["CHATID"], 'text': msg}
    requests.post(url, data)


# 使用pushplus发送推送信息
def send_pushplus(content, title):
    try:
        # TOKEN 放入 github 仓库 Secrets中
        token = os.environ["PUSH_PLUS_TOKEN"]
    except:
        # TOKEN 此处会明文暴露 ，不建议在此填写
        token = ''
    pattern = re.compile(r'\n')
    fail = re.compile(r'签到失败')
    content = re.sub(pattern, '<br/>', content)
    content = re.sub(fail, '<font style = "color:red">签到失败</font>', content)
    print(content)
    data = {'token': token, 'title': title, 'content': content}
    requests.post('http://pushplus.hxtrip.com/send/', data)
