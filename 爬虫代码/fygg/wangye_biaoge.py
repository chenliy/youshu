#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/8/1 16:28
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

from bs4 import BeautifulSoup
import requests
url = 'http://www.qzzjfy.gov.cn/?p=9822'
headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.qzzjfy.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
}

html = requests.get(url,headers=headers).text

soup = BeautifulSoup(html,'lxml')
trs = soup.find_all('tr')
result = []
for tr in trs:
    ui = []
    for td in tr:
        ui.append(td.string)
    result.append(ui)

print(result[6])
a = []
for x in result[6]:
    if x == '\n':
        pass
    else:
        a.append(x)
print(a)