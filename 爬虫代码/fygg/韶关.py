#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/8/4 9:10
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com
import requests
import json
class shaoguan():

    def get_csToken(self):
        r = requests.post(self.url_mm,data=self.data_mm,headers = self.headers_mm)
        print(r.status_code)
        csToken = eval(r.text).get("tokenVal",'a689e58760f4465ea42d4560da6c046b')
        print(csToken)
        return csToken

    def __init__(self):
        self.url_mm = 'http://sglccourts.gov.cn/common/getToKenTempPutCk'
        self.data_mm = {
            'tokenKey': '1808031025560986249'
        }
        self.headers_mm = {
            'Host': 'sglccourts.gov.cn',
            'Connection': 'keep-alive',
            'Content-Length': '28',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'http://sglccourts.gov.cn',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'http://sglccourts.gov.cn/web/search?action=gotoggxxcx&gglx=sdgg&flag=first',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': '__I18N_LOCALE__=zh_CN; 1533200178699=0E3F30963AA985FDD47CC7D06AF32BEB; JSESSIONID=B8E9023927AB3E6B164F240CCB28F865; 1533263029944=8BB99ED49F7D8955BD10978A0AE37ED6; 1533263137528=48BF5AD62D1E436EDD078DF43D05BD44; 1533263154792=8FBFD56BCD52AA0CA2A53ACC7FF3F99D'
        }
        self.csToken = self.get_csToken()
        self.url_xq = 'http://sglccourts.gov.cn/web/search?action=gotoggxxcx'
        self.data_xq = {
                'ah':'', #不变
                'fjm':'J20',#不变
                'gglx':'sdgg', #不变
                'xszt':'',#不变
                'ktzsfg':'',#不变
                'sjy':'',#不变
                'pagenumber':2,#当前页码数，可以遍历
                'dir':'down',#往下是down王上是up
                'csToken':self.csToken,#要变，主要问题就是要找出这个是从哪里来的：是另一个post 请求来的，而且是随机的
                'token_key':'1808031025560986249',#不变
        }
        self.headers_xq = {
    'Host': 'sglccourts.gov.cn',
    'Connection': 'keep-alive',
    'Content-Length': '134',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Origin': 'http://sglccourts.gov.cn',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'http://sglccourts.gov.cn/web/search?action=gotoggxxcx&gglx=sdgg&flag=first',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': '__I18N_LOCALE__=zh_CN; 1533200178699=0E3F30963AA985FDD47CC7D06AF32BEB; JSESSIONID=B8E9023927AB3E6B164F240CCB28F865; 1533263029944=8BB99ED49F7D8955BD10978A0AE37ED6; 1533263137528=48BF5AD62D1E436EDD078DF43D05BD44; 1533263154792=8FBFD56BCD52AA0CA2A53ACC7FF3F99D; 1808031025560986249={}'.format(self.csToken)

}

    def get_result(self):
        r = requests.post(self.url_xq,headers=self.headers_xq,data=self.data_xq)
        print(r.status_code,1)
        print(r.text)
        result = json.loads(r.text).get('ggList','')
        return result


t = shaoguan()
for x in t.get_result():
    defendant = x.get('SSDR', '')
    print(defendant)
    case_no = x.get('AH', '')
    print(case_no)
    ann_date = x.get('UPDATETIME', '')
    print(ann_date)
    announcer = x.get('FYMC', '')
    print(announcer)
    ann_html = str(x)
    print(ann_html)
    #content_url = 'http://sglccourts.gov.cn/web/search?action=gotoggxxcx#{}'.format(page)
    pdf_url = ''
