#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/8/7 12:47
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Referer': 'http://www.pyfy.gov.cn/index.php?m=content&c=index&a=lists&catid=46',
'Host': 'www.pyfy.gov.cn',
'Proxy-Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',

}
import requests
import time
url1 = 'http://www.pyfy.gov.cn/index.php?m=content&c=index&a=lists&catid=46'
url2 = 'http://www.pyfy.gov.cn/cdn-cgi/l/chk_jschl?jschl_vc=b54b9ac7b8d43e4eedd7eaba5e3b7703&pass=1533621370.796-nVtWQQM4%2BV&jschl_answer=14.6690253745'

r1 = requests.get(url1,headers)
print(1,r1.cookies)
cookies1 = r1.cookies
cookies = {'Cookie':'cfduid=d38f2f8c8a49c629473e7f1e85e171f2e1533622655&cf_clearance=f9b4ba34cec458b367045aa9ec787517ebd29396-1533621370-1800'}

time.sleep(5)
for i in range(10):
    r2 = requests.get(url2,headers,cookies=cookies)
    # cookies2 =r2.cookies
    print(2,r2.cookies)
    print(r2.text)
    time.sleep(2)
# r2_1 = requests.get(url2,headers,cookies = cookies2)
# print(r2_1.cookies)
# print(r2_1.text)
# # r2 = requests.get(url,headers,cookies = r.cookies)
# # print(r2.status_code)
# # print(r2.text)