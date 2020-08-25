import sys
import time
from typing import Optional

import requests
from bs4 import BeautifulSoup

person_list = [
    {
        'id': 'PBxxxxxxxx',  # 学号，必选
        'password': 'xxxxxxxx',  # 密码，必选
        'now_province': 'xx0000',  # 所在省份行政代号，如江苏省为 320000，可选，如没有这条则默认为安徽
        'now_city': 'xxxx00',  # 所在城市行政代号，如江苏南京为 320100，可选，如没有这条则默认为合肥
    },
    # ...
]

default_info = {
    'now_address': '1',
    'gps_now_address': '',
    'now_province': '340000',  # 安徽
    'gps_province': '',
    'now_city': '340100',  # 合肥
    'gps_city': '',
    'now_detail': '',
    'is_inschool': '6',  # 西区
    'body_condition': '1',  # 正常
    'body_condition_detail': '',
    'now_status': '1',  # 正常在校园内
    'now_status_detail': '',
    'has_fever': '0',
    'last_touch_sars': '0',
    'last_touch_sars_date': '',
    'last_touch_sars_detail': '',
    'last_touch_hubei': '0',
    'last_touch_hubei_date': '',
    'last_touch_hubei_detail': '',
    'last_cross_hubei': '0',
    'last_cross_hubei_date': '',
    'last_cross_hubei_detail': '',
    'return_dest': '1',
    'return_dest_detail': '',
    'other_detail': ''
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
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}


def get_full_data(person: dict) -> dict:
    info = default_info.copy()
    if 'now_province' in person:
        info['now_province'] = person['now_province']
    if 'now_city' in person:
        info['now_city'] = person['now_city']
    return info


def login(id: str, password: str) -> Optional[requests.Session]:
    url = 'https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fweixine.ustc.edu.cn%2F2020%2Fcaslogin'
    data = {
        'model': 'uplogin.jsp',
        'service': 'https://weixine.ustc.edu.cn/2020/caslogin',
        'username': id,
        'password': password
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
    if info.find('上次上报时间：2020-') is None:
        return False
    start = info.find('：') + 1
    date_str = info[start:start + len('2020-00-00')]
    if time.strftime("%Y-%m-%d", time.localtime()) == date_str:
        return True
    return False


def report(person: dict) -> bool:
    sess = login(person['id'], person['password'])
    if sess is None:
        return False
    if check_report(sess):
        return True
    r = sess.get('https://weixine.ustc.edu.cn/2020/home')
    soup = BeautifulSoup(r.text, 'html.parser')
    token = soup.find('input', {'name': '_token'})['value']
    if token is None:
        return False
    data = get_full_data(person)
    data['_token'] = token
    url = 'http://weixine.ustc.edu.cn/2020/daliy_report'
    headers['cookie'] = \
        f"PHPSESSID={sess.cookies.get('PHPSESSID')};" + \
        f"XSRF-TOKEN={sess.cookies.get('XSRF-TOKEN')};" + \
        f"laravel_session={sess.cookies.get('laravel_session')}"
    r = sess.post(url, data=data, headers=headers)
    if r.ok and check_report(sess):
        return True
    else:
        return False


if __name__ == '__main__':
    for person in person_list:
        try:
            success = report(person)
            if success:
                print(f"{person['id']} report successfully")
            else:
                print(f"{person['id']} report failed")
        except Exception as e:
            sys.stderr.write(str(e) + '\n')
