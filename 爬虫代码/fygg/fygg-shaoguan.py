#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/8/3 10:54
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

#post url

url = 'http://sglccourts.gov.cn/web/search?action=gotoggxxcx'


import requests

#csToken 就是 tokenVal，是来自另一个请求


print('#############################################')
url2 = 'http://sglccourts.gov.cn/common/getToKenTempPutCk'
url3 = 'http://sglccourts.gov.cn/common/getToKenTempPutCk'
headers_lb = {
'Host': 'sglccourts.gov.cn',
'Connection': 'keep-alive',
'Content-Length': '28',
'Accept': 'application/json, text/javascript, */*; q=0.01',
'Origin': 'http://sglccourts.gov.cn',
'X-Requested-With': 'XMLHttpRequest',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Referer': 'http://sglccourts.gov.cn/web/search?action=gotoggxxcx&gglx=sdgg&flag=first',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cookie': '__I18N_LOCALE__=zh_CN; 1533200178699=0E3F30963AA985FDD47CC7D06AF32BEB; JSESSIONID=B8E9023927AB3E6B164F240CCB28F865; 1533263029944=8BB99ED49F7D8955BD10978A0AE37ED6; 1533263137528=48BF5AD62D1E436EDD078DF43D05BD44; 1533263154792=8FBFD56BCD52AA0CA2A53ACC7FF3F99D'
}

data2 = {
'tokenKey':'1808031025560986249'
}
r2 =requests.post(url2,headers=headers_lb,data=data2)
print(r2.status_code)
print(r2.text)
csToken = eval(r2.text).get("tokenVal",'')
print(csToken)


data = {
    'ah':'', #不变
    'fjm':'J20',#不变
    'gglx':'sdgg', #不变
    'xszt':'',#不变
    'ktzsfg':'',#不变
    'sjy':'',#不变
    'pagenumber':4,#当前页码数，可以遍历
    'dir':'down',#往下是down王上是up
    'csToken':'a689e58760f4465ea42d4560da6c046b',#要变，主要问题就是要找出这个是从哪里来的：是另一个post 请求来的，而且是随机的
    'token_key':'1808031025560986249',#不变
}
headers_xq = {
    'Host': 'sglccourts.gov.cn',
    'Connection': 'keep-alive',
    'Content-Length': '100',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Origin': 'http://sglccourts.gov.cn',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'http://sglccourts.gov.cn/web/search?action=gotoggxxcx&gglx=sdgg&flag=first',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': '__I18N_LOCALE__=zh_CN; 1533200178699=0E3F30963AA985FDD47CC7D06AF32BEB; JSESSIONID=B8E9023927AB3E6B164F240CCB28F865; 1533263029944=8BB99ED49F7D8955BD10978A0AE37ED6; 1533263137528=48BF5AD62D1E436EDD078DF43D05BD44; 1533263154792=8FBFD56BCD52AA0CA2A53ACC7FF3F99D; 1808031025560986249=a689e58760f4465ea42d4560da6c046b'

}
r = requests.post(url,headers=headers_xq,data=data)
print(r.status_code)
print(r.text)
