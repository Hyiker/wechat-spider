#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

from bs4 import BeautifulSoup
from requests import Session


def query_biz_by_name(session, account):
    url = 'https://weixin.sogou.com/weixin?query={}'.format(account)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.132 Safari/537.36 '
    }
    session.headers = headers
    resp = session.get(url=url, headers=headers).text
    search_soup = BeautifulSoup(resp, 'html.parser')
    if search_soup.select_one('#noresult_part1_container') is not None:
        # 没有查询到对应公众号
        return None
    profile_url = 'https://weixin.sogou.com/{}'.format(
        search_soup.select_one('.news-list2 > li > div > .txt-box > p > a')['href'])
    response = session.get(profile_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    if response.status_code == 302:
        # 跳转入验证码页
        verify_code_url = soup.select_one('#seccodeImage')['src']
    else:
        print('未出现验证码')
        print(response.content.decode('utf-8'))
        res = re.findall('.*var biz = "(.*)" \|\| "";.*', response.text)
        print(res)


query_biz_by_name(Session(), '软风知芯')
