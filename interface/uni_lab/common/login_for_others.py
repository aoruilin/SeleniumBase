import requests
from base.data import Ips
from base.data import UnPw

ip = Ips.ip_for_uniLab
URL = ip + '/pc/login'
HEADERS = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/68.0.3440.84 Safari/537.36'
}
username = UnPw.username_for_uniLab
password = UnPw.password_for_uniLab
DATA = {
    "password": password,
    "username": username
}

def login_interface(url=URL, data=DATA, headers=HEADERS):
    '''提供公用的token'''
    t = requests.session()
    login_ret = t.post(url=url, headers=headers, json=data)
    token = login_ret.json()['data']['token']
    return token

# print(login_interface())