#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/19 17:00
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com


#第二页
'https://www.mzcourt.gov.cn/courtweb/front/wsxxList?ah=&ay=&fjm=JC0&dsr=&wsmc=&wslx=qbcpws&pagenumber=1&dir=down&cs_token_flag=1&cs_token=7775c3a0dedd489c973fb6289a8f0d8d'
'https://www.mzcourt.gov.cn/courtweb/front/wsxxList?ah=&ay=&fjm=JC0&dsr=&wsmc=&wslx=qbcpws&pagenumber=1&dir=down&cs_token_flag=1&cs_token=7775c3a0dedd489c973fb6289a8f0d8d'
#第一页
url2 = 'https://www.mzcourt.gov.cn/courtweb/front/wsxxList?ah=&ay=&fjm=JC0&dsr=&wsmc=&wslx=qbcpws&pagenumber=2&dir=up&cs_token_flag=1&cs_token=7775c3a0dedd489c973fb6289a8f0d8d'

import requests
headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Cookie': 'JSESSIONID=64ACB1A0DD743A5065637998D42CB269; __I18N_LOCALE__=zh_CN; JC0css2018071916295850838997=35AE8F811939FFBA64558D88DC84EC07; JC0css2018071916302326155489=30DF29209BC378EFED70857E6FDBD7CC; JC0css2018071916302952758457=C8EA59FDFA81BF597C473F4E1E736BE7; JC0css2018071916303324530338=978A2A15FE4375363279917C4C561831; JC0css2018071916303693303223=D36D981F1B2A32D2AED99A42F826B8E0',
            'Host': 'www.mzcourt.gov.cn',
            'Referer': 'https://www.mzcourt.gov.cn/courtweb/front/wsxxList?ah=&ay=&fjm=JC0&dsr=&wsmc=&wslx=qbcpws&pagenumber=3&dir=down&cs_token_flag=1&cs_token=7775c3a0dedd489c973fb6289a8f0d8d',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
        }
html = requests.get(url=url2,headers = headers ,verify=False).text
print(html)