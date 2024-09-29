# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

URL='https://sso.cup.edu.cn/login?service=https%3A%2F%2Fsct.cup.edu.cn%2Fucenter%2Findex%2Fsaveticket'
USERNAME = 'your_username'
PASSWORD = 'your_password'

get_7da9a_headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Connection': 'keep-alive',
    'Host': 'sso.cup.edu.cn',
    'User-Agent': ''
}

login_headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Connection': 'keep-alive',
    'Host': 'sso.cup.edu.cn',
    'Origin': 'https://sso.cup.edu.cn',
    'Referer': 'https://sso.cup.edu.cn/login?service=https%3A%2F%2Fsct.cup.edu.cn%2Fucenter%2Findex%2Fsaveticket',
    'User-Agent': ''
}

after_login_headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Connection': 'keep-alive',
    'Host': 'sct.cup.edu.cn',
    'Referer': 'https://sso.cup.edu.cn/',
    'User-Agent': ''
}


def get__7da9a():
    session = requests.session()
    response = session.get(URL,headers=get_7da9a_headers)
    print(response)
    item = response.headers.get('Set-Cookie').split(';')[0].split('=')
    _7da9a_cookie={
        '_7da9a':item[1]
    }
    return  _7da9a_cookie


def login(cookies):
    session = requests.session()
    response = session.get(URL, headers=login_headers, cookies=cookies)
    # 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找 execution 字段
    execution_input = soup.find('input', {'name': 'execution'})
    execution_value = ''
    if execution_input:
        execution_value = execution_input['value']
        print(f'获取的 execution 值: {execution_value}')
    else:
        print('未找到 execution 字段。')

    payload = {
        'username': USERNAME,
        'password': PASSWORD,
        'execution': execution_value,
        '_eventId': 'submit',  # 根据实际情况调整
        'submit': '%E7%99%BB%E5%BD%95',
        'type': 'username_password'
        # 根据实际需要添加其他字段
    }

    response = session.post(URL, data=payload, headers=login_headers, cookies=cookies,
                            allow_redirects=False)  # 返回302是正确的
    if 'Location' in response.headers:
        redirect_url = response.headers['Location']
        response = session.get(redirect_url,headers=after_login_headers)
        PHPSESSID=session.cookies.get('PHPSESSID')
        return PHPSESSID
    return False

def get_cookies():
    cookies = get__7da9a()
    return login(cookies)

if __name__ == '__main__':
    cookies=get__7da9a()
    login(cookies)
