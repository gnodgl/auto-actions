import random
import re
from auto_sign.config import generateConfig


# 投票签到
def vote(session, url):
    id_url = url + "/index.php"
    with session.get(id_url) as index:
        h = re.compile(r'funvote\((.*?),\'fun\'\)')
        i = re.compile(r'<span id="funvote"><b>(.*?)</b>')
        if i.search(index.text):
            print("已投票")
        elif h.search(index.text):
            id_param = h.search(index.text).group(1)
            vote_param = random.choice(['fun', 'dull'])
            vote_url = url + "/fun.php?action=vote&id=" + id_param + "&yourvote=" + vote_param
            session.get(vote_url)
            print("投票成功")


def main():
    [vote(config['session'], config['url']) for config in generateConfig() if 'vote' in config['tasks']]


if __name__ == '__main__':
    main()
