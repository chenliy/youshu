#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/25 15:30
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

import requests
import random
import re
from pyquery import PyQuery as pq

schema_def = [{"name": "id", "type": "string"},
              {"name": "_id_", "type": "string"},
              {"name": "ann_type", "type": "string"},
              {"name": "announcer", "type": "string"},
              {"name": "case_no", "type": "string"},
              {"name": "ann_content", "type": "string"},
              {"name": "ann_date", "type": "string"},
              {"name": "content_url", "type": "string"},
              {"name": "ann_html", "type": "string"},
              {"name": "pdf_url", "type": "string"},
              {"name": "source", "type": "string"},
              {"name": "defendant", "type": "string"},
              ]

UA = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'eedszy.chinacourt.org',
            'Cookie':'Hm_lvt_c32eb45d9f69afbc206e06d63e668e75=1531708352,1532483935,1532509683; PHPSESSID=1vi209svv9b2vu5p0kc0tp6th0',
            'Referer':'http://eedszy.chinacourt.org/article/index/id/MzAsMTDINSAOAAA.shtml',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': random.choice(UA),
        }

proxies = {
        'http': 'http://H21WNK49K6PFSR3P:BF2B9DDE973F0C02@http-pro.abuyun.com:9010',
        'https': 'https://H21WNK49K6PFSR3P:BF2B9DDE973F0C02@http-pro.abuyun.com:9010',
        'Proxy-Switch-Ip': 'yes'
    }

for i in range(1,2):
    url = 'http://eedszy.chinacourt.org/article/index/id/MzAsMTDINSAOAAA/page/{}.shtml'.format(i)
    r = requests.get(url,headers=headers,proxies=proxies)
    print(len(r.text))

    p = pq(r.text)
    urls = []
    for each in p('span.left a[href]').items():
        print(each.attr['href'])
        url = 'http://eedszy.chinacourt.org' + each.attr['href']
        urls.append(url)
    for url in urls:
        r = requests.get(url,headers=headers,proxies=proxies)
        if r.status_code == 200:
            p = pq(r.text)
            for each in p('div.yui-g').items():
                print(each.text())
                print(each.text().split('\n'))


        else:
            print(r.status_code)
            continue

