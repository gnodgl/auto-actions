import json
import re
from json.decoder import JSONDecodeError

from auto_sign.config import generateConfig
from auto_sign.utility.function import now, nowstamp, sendQmsgInfo, send_telegram

txt = now()+" PT签到\n"


def signin(session, url, name):
    # 完整签到url
    global txt
    # hdarea签到
    if url == "https://www.hdarea.co":
        attendance_url = url + '/sign_in.php'
        data = {"action": "sign_in"}
        with session.post(attendance_url, data) as res:
            r = re.compile(r'获得了\d+魔力值')
            r1 = re.compile(r'重复')
            print(res.text)
            if r.search(res.text):
                tip = ' 签到成功'
            elif r1.search(res.text):
                tip = ' 重复签到'
            else:
                tip = 'cookie已过期'
            print(now(), ' 网站：%s' % url, tip)
            txt += '网站：<a href="%s">%s</a>' % (url, name) + tip + '\n'
    # 猫站签到
    elif url == "https://pterclub.com":
        attendance_url = url + '/attendance-ajax.php'
        with session.get(attendance_url) as res:
            try:
                msg = json.loads(res.text.encode('utf-8').decode('unicode-escape')).get('message')
            except JSONDecodeError:
                msg = res.text
            if '连续签到' in msg:
                tip = ' 签到成功'
            elif '重复刷新' in msg:
                tip = ' 重复签到'
            else:
                tip = ' cookie已过期'
            print(now(), ' 网站：%s' % url, tip)
            txt += '网站：<a href="%s">%s</a>' % (url, name) + tip + '\n'
    # 海胆签到
    elif url == "https://www.haidan.video":
        attendance_url = url + '/signin.php'
        with session.get(attendance_url) as res:
            r = re.compile(r'已经打卡')
            r1 = re.compile(r'退出')
            if r.search(res.text):
                tip = ' 签到成功'
            elif r1.search(res.text):
                tip = ' 重复签到'
            else:
                tip = ' cookie已过期!'
            print(now(), ' 网站：%s' % url, tip)
            txt += '网站：<a href="%s">%s</a>' % (url, name) + tip + '\n'
    # bschool
    elif url == "https://pt.btschool.club":
        attendance_url = url + '/index.php?action=addbonus'
        with session.get(attendance_url) as res:
            r = re.compile(r'今天签到您获得\d+点魔力值')
            r1 = re.compile(r'退出')
            if r.search(res.text):
                tip = ' 签到成功'
            elif r1.search(res.text):
                tip = ' 重复签到'
            else:
                tip = ' cookie已过期'
            print(now(), ' 网站：%s' % url, tip)
            txt += '网站：<a href="%s">%s</a>' % (url, name) + tip + '\n'
    # lemonhd
    elif url == "https://lemonhd.org":
        attendance_url = url + '/attendance.php'
        with session.get(attendance_url) as res:
            r = re.compile(r'已签到')
            r1 = re.compile(r'请勿重复刷新')
            # print(res.text)
            if r.search(res.text) and r1.search(res.text) is None:
                tip = ' 签到成功'
            elif r1.search(res.text):
                tip = ' 重复签到'
            else:
                tip = ' cookie已过期'
            print(now(), ' 网站：%s' % url, tip)
            txt += '网站：<a href="%s">%s</a>' % (url, name) + tip + '\n'
    # hares白兔
    elif url == "https://club.hares.top":
        attendance_url = url + '/attendance.php?action=sign'
        headers = {'Accept': 'application/json'}
        session.headers.update(headers)
        # print(session.headers)
        with session.get(attendance_url) as res:
            try:
                msg = json.loads(res.text.encode('utf-8').decode('unicode-escape')).get('msg')
            except JSONDecodeError:
                msg = res.text
            r = re.compile(r'签到成功')
            r1 = re.compile(r'已经签到')
            print(msg)
            if r.search(msg) and r1.search(msg) is None:
                tip = ' 签到成功'
            elif r1.search(msg):
                tip = ' 重复签到'
            else:
                tip = ' cookie已过期'
            print(now(), ' 网站：%s' % url, tip)
            txt += '网站：<a href="%s">%s</a>' % (url, name) + tip + '\n'
    else:
        attendance_url = url + '/attendance.php'
        # 绕过cf5秒盾
        # session = cloudscraper.create_scraper(session)
        with session.get(attendance_url) as res:
            r = re.compile(r'请勿重复刷新')
            r1 = re.compile(r'签到已得[\s]*\d+')
            # if url == "https://www.hddolby.com" or url == "https://pt.btschool.club":
            # print(res.text)
            if r.search(res.text):
                tip = ' 重复签到'
            elif r1.search(res.text):
                tip = ' 签到成功'
            else:
                tip = ' cookie已过期'
            print(now(), ' 网站：%s' % url, tip)
            txt += '网站：<a href="%s">%s</a>' % (url, name) + tip + '\n'


# discuz系列签到
def signin_discuz_dsu(session, url, name):
    attendance_url = url + "/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&sign_as=1&inajax=1"
    hash_url = url + "/plugin.php?id=dsu_paulsign:sign"
    with session.get(hash_url) as hashurl:
        h = re.compile(r'name="formhash" value="(.*?)"')
        formhash = h.search(hashurl.text).group(1)
    data = {"qdmode": 3, "qdxq": "kx", "fastreply": 0, "formhash": formhash, "todaysay": ""}
    with session.post(attendance_url, data) as res:
        r = re.compile(r'签到成功')
        r1 = re.compile(r'已经签到')
        global txt
        if r.search(res.text):
            txt += '网站：<a href="%s">%s</a>' % (url, name) + " 签到成功 \n"
            print(now(), ' 网站：%s' % url, " 签到成功")
        elif r1.search(res.text):
            txt += '网站：<a href="%s">%s</a>' % (url, name) + " 重复签到 \n"
            print(now(), ' 网站：%s' % url, " 重复签到")
        else:
            txt += '网站：<a href="%s">%s</a>' % (url, name) + " cookie已过期 \n"
            print(now(), ' 网站：%s' % url, res.text)


# 不移之火签到
def signin_discuz_ksu(session, url, name):
    attendance_url = url + "/plugin.php?id=k_misign:sign&operation=qiandao"
    hash_url = url + "/plugin.php?id=k_misign:sign"
    with session.get(hash_url) as hashurl:
        h = re.compile(r'name="formhash" value="(.*?)"')
        print(hashurl.text)
        formhash = h.search(hashurl.text).group(1)
    data = {"formhash": formhash, "format": "empty"}
    with session.post(attendance_url, data) as res:
        # print(res.text)
        r = re.compile(r'CDATA\[\]')
        r1 = re.compile(r'今日已签')
        global txt
        if r.search(res.text):
            txt += '网站：<a href="%s">%s</a>' % (url, name) + " 签到成功 \n"
            print(now(), ' 网站：%s' % url, " 签到成功")
        elif r1.search(res.text):
            txt += '网站：<a href="%s">%s</a>' % (url, name) + " 重复签到 \n"
            print(now(), ' 网站：%s' % url, " 重复签到")
        else:
            txt += '网站：<a href="%s">%s</a>' % (url, name) + " cookie已过期 \n"
            print(now(), ' 网站：%s' % url, res.text)


# hifi签到
def signin_hifi(session, url, name):
    attendance_url = url + "/sg_sign.htm"
    with session.post(attendance_url) as res:
        r = re.compile(r'成功')
        r1 = re.compile(r'今天已经')
        global txt
        if r.search(res.text):
            txt += '网站：<a href="%s">%s</a>' % (url, name) + " 签到成功 \n"
            print(now(), ' 网站：%s' % url, " 签到成功")
        elif r1.search(res.text):
            txt += '网站：<a href="%s">%s</a>' % (url, name) + " 重复签到 \n"
            print(now(), ' 网站：%s' % url, " 重复签到")
        else:
            txt += '网站：<a href="%s">%s</a>' % (url, name) + " cookie已过期 \n"
            print(now(), ' 网站：%s' % url, res.text)


def main():
    global txt
    print(now(), '--PT站开始签到--')
    [signin(config['session'], config['url'], config['name']) for config in generateConfig() if 'sign_in' in config['tasks']]
    print(now(), '--其他站开始签到--')
    [signin_discuz_dsu(config['session'], config['url'], config['name']) for config in generateConfig() if 'sign_in_discuz' in config['tasks']]
    [signin_hifi(config['session'], config['url'], config['name']) for config in generateConfig() if 'sign_in_hifi' in config['tasks']]
    [signin_discuz_ksu(config['session'], config['url'], config['name']) for config in generateConfig() if 'sign_in_discuz_ksu' in config['tasks']]
    # cookie过期发送qq推送信息
    r = re.compile(r'过期')
    r1 = re.compile(r'重复')
    if r.search(txt) or r1.search(txt):
        # sendQmsgInfo(txt)
        send_telegram(txt)



if __name__ == '__main__':
    main()
