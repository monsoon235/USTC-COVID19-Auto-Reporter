import datetime
import sys
from typing import List, Optional

import pytz
import requests
import yaml
from bs4 import BeautifulSoup

default_info = {
    'now_address': '1',  # 当前所在地 1:内地 2:香港 3:国外 4:澳门 5:台湾
    'gps_now_address': '',
    'now_province': '340000',  # 当前省份代码，默认安徽
    'gps_province': '',
    'now_city': '340100',  # 当前城市代码，默认合肥
    'gps_city': '',
    'now_detail': '',  # 具体位置，当前所在地为“国外”时填写
    'is_inschool': '6',  # 是否在校 0:校外 2:东区 3:南区 4:中区 5:北区 6:西区
    'body_condition': '1',  # 当前身体状况 1:正常 2:疑似 3:确诊 4:其他
    'body_condition_detail': '',  # 具体情况，当前身体状况为“其他”时填写
    'now_status': '1',  # 当前状态 1:正常在校园内 2:正常在家 3:居家留观 4:集中留观 5:住院治疗 6:其他
    'now_status_detail': '',  # 具体情况，当前状态选择“其他”时填写
    'has_fever': '0',  # 目前有无发热症状 0:无 1: 有
    'last_touch_sars': '0',  # 是否接触过疑似患者  0:无 1:有
    'last_touch_sars_date': '',  # 最近一次接触日期，当是否接触过疑似患者为“有”时填写
    'last_touch_sars_detail': '',  # 具体情况，当是否接触过疑似患者为“有”时填写
    'other_detail': ''  # 其他情况说明
}

headers = {
    'authority': 'weixine.ustc.edu.cn',
    'method': 'POST',
    'path': '/2020/daily_report',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://weixine.ustc.edu.cn',
    'referer': 'https://weixine.ustc.edu.cn/2020/home',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
}


def read_info() -> List[dict]:
    with open('info.yaml') as f:
        info = yaml.load(f, Loader=yaml.FullLoader)
    for i in range(len(info)):
        full = default_info.copy()
        full.update(info[i])
        info[i] = full
    return info


def login(id: str, password: str) -> Optional[requests.Session]:
    url = 'https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fweixine.ustc.edu.cn%2F2020%2Fcaslogin'
    data = {
        'model': 'uplogin.jsp',
        'service': 'https://weixine.ustc.edu.cn/2020/caslogin',
        'warn': '',
        'showCode': '',
        'username': id,
        'password': password,
        'button': ''
    }
    sess = requests.Session()
    r = sess.post(url, data=data)
    if r.url == 'https://weixine.ustc.edu.cn/2020/home':
        print(f'{id} login successfully')
        return sess
    else:
        print(f'{id} login failed')
        return None


def check_report(sess: requests.Session) -> bool:
    r = sess.get('https://weixine.ustc.edu.cn/2020/home')
    soup = BeautifulSoup(r.text, 'html.parser')
    info = soup.find('span', {'style': 'position: relative; top: 5px; color: #666;'})
    if info is None:
        return False
    info = info.text
    if info.find('上次上报时间：') is None:
        return False
    start = info.find('：') + 1
    date_str = info[start:start + len('0000-00-00')]
    date_remote = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    date_local = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).date()
    if date_remote == date_local:
        return True
    return False


def report(info: dict, check_first: bool = True) -> bool:
    data = info.copy()
    sess = login(data['id'], data['password'])
    data.pop('id')
    data.pop('password')
    if sess is None:
        return False
    if check_first and check_report(sess):
        return True
    r = sess.get('https://weixine.ustc.edu.cn/2020/home')
    soup = BeautifulSoup(r.text, 'html.parser')
    token = soup.find('input', {'name': '_token'})['value']
    if token is None:
        return False
    data['_token'] = token
    url = 'http://weixine.ustc.edu.cn/2020/daliy_report'
    headers['cookie'] = \
        f"PHPSESSID={sess.cookies.get('PHPSESSID')};" + \
        f"XSRF-TOKEN={sess.cookies.get('XSRF-TOKEN')};" + \
        f"laravel_session={sess.cookies.get('laravel_session')}"
    r = sess.post(url, data=data)  # , headers=headers)
    if r.ok and check_report(sess):
        return True
    else:
        return False


if __name__ == '__main__':
    for info in read_info():
        try:
            success = report(info, check_first=False)
            if success:
                print(f"{info['id']} report successfully")
            else:
                print(f"{info['id']} report failed")
        except Exception as e:
            sys.stderr.write(str(e) + '\n')
