#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/17 9:43
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

#每一页url 都保持不变
import datetime
#首页
url0 = 'http://www.sdcourt.gov.cn/sdfy/1251908/index.html'

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '1046',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'wenshu.court.gov.cn',
    'Origin': 'http://wenshu.court.gov.cn',
    'Referer':'http://wenshu.court.gov.cn/list/list/?sorttype=1&conditions=searchWord+%E5%B1%B1%E4%B8%9C%E7%9C%81%E9%AB%98%E7%BA%A7%E4%BA%BA%E6%B0%91%E6%B3%95%E9%99%A2+SLFY++%E6%B3%95%E9%99%A2%E5%90%8D%E7%A7%B0:%E5%B1%B1%E4%B8%9C%E7%9C%81%E9%AB%98%E7%BA%A7%E4%BA%BA%E6%B0%91%E6%B3%95%E9%99%A2',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

import requests

html1 = requests.get(url0,headers=headers).text
print(html1)
datetime.datetime.strftime()
