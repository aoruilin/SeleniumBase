import requests
from interface.uni_lab.common.login_for_others import login_interface
from base.data import Ips

ip = Ips.ip_for_uniLab
URL = ip + '/pc/clbum/self/list'
HEADERS = {
    'Content-Type': 'application/json',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
}

def getClassList(url=URL,headers=HEADERS):
    '''提供公用的classid'''
    token = login_interface()
    headers['token'] = token
    response = requests.get(url=url, headers=headers)
    classList_ret = response.json()
    data_dic = classList_ret['data']
    data = data_dic[0]
    classId_list = []
    classId = data['clbumId']
    classId_list.append(classId)
    return classId_list

print(getClassList())