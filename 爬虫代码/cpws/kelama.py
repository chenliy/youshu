#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/25 11:00
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

import requests
import re

headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'fy.klmyq.gov.cn',
            'Referer': 'http://fy.klmyq.gov.cn/rmfy_txlist.jsp?a3t=4&a3p=2&a3c=15&urltype=tree.TreeTempUrl&wbtreeid=26853',
            'Upgrade-Insecure-Requests': '1',
            'Cookie': 'ant_stream_50918e23b6ea0=1532514922/2485061470; bow_stream_50918e23b6ea0=13; JSESSIONID=09501E96D7B3FE7752C6C334402E5590',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
}

url = 'http://fy.klmyq.gov.cn/rmfy_txlist.jsp?a3t=4&a3p=3&a3c=15&urltype=tree.TreeTempUrl&wbtreeid=26853'
r = requests.get(url,headers=headers).text
print(r)