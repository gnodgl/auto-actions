#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import requests
import configparser

from auto_sign.utility.function import cookieParse


def generateHeader(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': url
    }
    return header


def generateConfig():
    # 获取cookie , 环境变量取不到就到配置文件取
    try:
        # COOKIE JSON 格式放入 github 仓库 Secrets中
        config_str = os.environ["CONFIG"]
    except:
        # COOKIE DICT 格式在此填写 ，此处会明文暴露 ，不建议在此填写
        config_obj = configparser.RawConfigParser()
        config_obj.read('config.ini', encoding='utf-8')
        config_str = config_obj['NexusPHP']['config']

    configs = eval(config_str)

    for config in configs:
        config['cookie'] = cookieParse(config['cookie'])

        header = generateHeader(config['url'])

        # 设置请求头 、 cookie
        session = requests.session()
        session.headers.update(header)
        session.cookies.update(config['cookie'])

        yield {'url': config['url'], 'session': session, 'tasks': config['tasks'], 'name': config['name']}


if __name__ == '__main__':
    [print(config) for config in generateConfig()]
