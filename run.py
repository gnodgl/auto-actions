import sys
from auto_sign.tasks.pt_say_thanks import main as saythanks
from auto_sign.tasks.pt_sign import main as signin
from auto_sign.tasks.tieba import main as tieba
from auto_sign.tasks.v2ex import go_sign as v2ex
from auto_sign.tasks.vote import main as vote
from auto_sign.tasks.shout import main as shout
from auto_sign.tasks.smzdm_sign import checkin as smzdm

if __name__ == '__main__':
    action = sys.argv[1]
    eval('%s()' % action)
