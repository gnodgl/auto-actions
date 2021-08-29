import configparser
import logging
import os
import re

import requests

from auto_sign.utility.function import now, sendQmsgInfo

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'zhiyou.smzdm.com',
    'Referer': 'https://www.smzdm.com/',
    'Sec-Fetch-Dest': 'script',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

# 测试cookies
TEST_COOKIE = ''

# 签到url
CHECK_IN_URL = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'

MSG = now()+' SMZDM签到\n'


# 定义session
def makesession():
    # 环境变量获取cookies
    # cookies = os.environ["SMZDM_COOKIES"]
    try:
        # COOKIE JSON 格式放入 github 仓库 Secrets中
        cookies = os.environ["SMZDM_COOKIES"]
    except:
        # COOKIE DICT 格式在此填写 ，此处会明文暴露 ，不建议在此填写
        config_obj = configparser.RawConfigParser()
        config_obj.read('config.ini')
        cookies = config_obj['SMZDM']['cookie']
    # cookies = TEST_COOKIE
    session = requests.session()
    session.headers = HEADERS
    session.headers['Cookie'] = cookies
    return session


# 签到函数
def checkin():
    global MSG
    with makesession().get(CHECK_IN_URL) as res:
        try:
            result = res.json()['data']['slogan']
            r = re.compile(r'已签到')
            r1 = re.compile(r'今日已领')
            if r.search(result):
                logger.info('签到成功')
                tip = '签到成功'
            elif r1.search(result):
                tip = '重复签到'
            else:
                tip = ' cookie已过期'
            MSG += tip
            print(MSG)
        except Exception as e:
            logger.error('签到失败! \n'+'返回数据:'+res.text+'\n'+f'异常 : {e}')


if __name__ == '__main__':
    checkin()
