import configparser
import logging
import os
import re

import requests

from auto_sign.utility.function import now, cookieParseV2ex, sendQmsgInfo

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

HEADERS = {
    'Referer': 'https://www.v2ex.com/mission',
    'Host': 'www.v2ex.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
}



CHECK_URL = 'https://www.v2ex.com/mission/daily'

BALANCE_URL = 'https://www.v2ex.com/balance'

SIGN_URL = 'https://www.v2ex.com/mission/daily/redeem?once='

ONCE = None

CKSTATUS = 1

SIGNSTATUS = 0

MSG = now()+' V2EX签到\n'


# 定义session
def makesession():
    # 环境变量获取cookies
    try:
        # COOKIE JSON 格式放入 github 仓库 Secrets中
        cookies_str = os.environ["V2EX_COOKIES"]
    except:
        # COOKIE DICT 格式在此填写 ，此处会明文暴露 ，不建议在此填写
        config_obj = configparser.RawConfigParser()
        config_obj.read('config.ini')
        cookies_str = config_obj['V2EX']['cookie']
    # cookies_str = os.environ["V2EX_COOKIES"]
    cookies = cookieParseV2ex(cookies_str)
    session = requests.session()
    session.headers.update(HEADERS)
    session.cookies.update(cookies)
    return session


# 查询是否签到获取once参数
def check():
    global CKSTATUS, MSG, SIGNSTATUS
    with makesession().get(CHECK_URL) as res:
        r = re.compile(r'需要先登录')
        r1 = re.compile(r'每日登录奖励已领取')
        r2 = re.compile(r"redeem\?once=(.*?)'")
        tip = r.search(res.text).group() if r.search(res.text) else '已登录'
        tip1 = r1.search(res.text).group() if r1.search(res.text) else '今天已经签到过啦'
        if '需要先登录' == tip:
            logger.info('V2EXcookies失效')
            CKSTATUS = 2
            MSG += 'cookies失效了!\n'
        elif '每日登录奖励已领取' == tip1:
            logger.info('今天已经签到过啦')
            CKSTATUS = 0
            SIGNSTATUS = 1
            MSG += '今天已经签到过啦\n'
        else:
            global ONCE
            ONCE = r2.search(res.text).group(1) if r2.search(res.text) else '没有找到once'


# 签到
def sign():
    global MSG, SIGNSTATUS
    with makesession().get(SIGN_URL+ONCE) as res:
        r = re.compile(r'已成功领取每日登录奖励')
        tip = r.search(res.text).group() if r.search(res.text) else '签到失败'

        if r.search(res.text):
            logger.info('签到成功')
            SIGNSTATUS = 1
            MSG += '签到成功\n'
        else:
            logger.error('签到失败!')
            MSG += '签到失败\n'


# 查询余额
def balance():
    global MSG
    with makesession().get(BALANCE_URL) as res:
        r = re.compile(r'\d+?\s的每日登录奖励\s\d+\s铜币')
        tip = r.search(res.text).group() if r.search(res.text) else '铜币查询失败'
        if '铜币查询失败' == tip:
            MSG += '铜币查询失败\n'
        else:
            logger.info(tip)
            MSG += tip


# 签到流程
def go_sign():
    global MSG, CKSTATUS, ONCE, SIGNSTATUS
    logger.info('V2EX开始签到!')
    check()
    if CKSTATUS == 1:
        if (ONCE is not None) & SIGNSTATUS == 0:
            sign()
            if SIGNSTATUS == 0:
                check()
                sign()

    if CKSTATUS != 2:
        balance()
    r = re.compile(r'cookies')
    # 判断是否发送通知
    if r.search(MSG):
        sendQmsgInfo(MSG)


if __name__ == '__main__':
    go_sign()
