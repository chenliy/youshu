#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/23 18:03
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

import requests
from pyquery import PyQuery as pq

headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.sxcourt.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
        }

url = 'http://www.sxcourt.gov.cn/E_ReadNews.asp?NewsID=7456'
url2 = 'http://www.sxcourt.gov.cn/E_ReadNews.asp?NewsID=7744'
r = requests.get(url=url2,headers=headers)
r.encoding = r.apparent_encoding
html = r.text
p = pq(html)

court_name = []
for each in p('#zoom > p:nth-child(1)').items():
    court_name.append(each.text())
    print(each.text())
print(court_name[0].replace('\n',''))
print(len(court_name))

type0 = []
for each in p('#zoom > p:nth-child(2)').items():
    type0.append(each.text())
    print(each.text(),2)
print(type0[0].replace('\n',''))

case_no = []
for each in p('#zoom > p:nth-child(4)').items():
    case_no.append(each.text())
    print(each.text(),2)
print(case_no[0].replace('\n',''))

for each in p('#zoom > p:nth-child(3)').items():
    if each.text():
        print(1)
    else:
        print(2)