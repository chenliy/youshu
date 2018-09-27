#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/9 15:26
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com


import requests
url = 'http://www.baidu.com'
headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection':'keep-alive',
            'If-Modified-Since': 'Mon, 09 Jul 2018 01:19:09 GMT',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
        }

r = requests.get(url,headers = headers)
print(r.status_code)

import datetime
a = datetime.timedelta(days=1)
print(a)

b = u'dfds'
print(b)