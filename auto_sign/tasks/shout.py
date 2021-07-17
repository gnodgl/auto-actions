import random
import re
from auto_sign.config import generateConfig
from auto_sign.utility.function import now, sendQmsgInfo

txt = now()+" 吼吼箱签到\n"


# 吼吼箱签到
def shout(session, url):
    attendance_url = url + "/shoutbox.php"
    shouttext = random.choice(['[em4]', '[em5]', '[em8]', '[em10]'])
    text = "签到"+shouttext
    attendance_url += "?shbox_text="+text+"&shout=我喊&sent=yes&type=shoutbox"
    with session.post(attendance_url) as res:
        r = re.compile(r'登录')
        global txt
        if r.search(res.text):
            txt += '网站：%s' % url + "cookie已过期 \n"
            print(now(), ' 网站：%s' % url, res.text)
        else:
            txt += '网站：%s' % url + " 签到成功 \n"
            print(now(), ' 网站：%s' % url, "签到成功")


def main():
    [shout(config['session'], config['url']) for config in generateConfig() if 'shout' in config['tasks']]
    # cookie过期发送qq推送信息
    r = re.compile(r'过期')
    if r.search(txt):
        sendQmsgInfo(txt)


if __name__ == '__main__':
    main()
