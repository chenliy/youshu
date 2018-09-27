#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/8/4 10:58
# Project:
# @Author: ZQJ
# @Email : zihe@yscredit.com

from pyspider.libs.base_handler import *
import requests
import json


class Handler(BaseHandler):
    crawl_config = {
        'itag': 'v7.30'
    }
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
                  {"name": "defendant", "type": "string"}
                  ]

    def get_csToken(self):
        r = requests.post(self.url_mm, data=self.data_mm, headers=self.headers_mm)
        print(r.status_code)
        csToken = eval(r.text).get("tokenVal", 'a689e58760f4465ea42d4560da6c046b')
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

        self.url_xq = 'http://sglccourts.gov.cn/web/search?action=gotoggxxcx'

    def get_result(self):
        r = requests.post(self.url_xq, headers=self.headers_xq, data=self.data_xq)
        print(r.status_code, 1)
        print(r.text)
        result = json.loads(r.text).get('ggList', '')
        return result

    @every(minutes=24 * 60)
    def on_start(self):
        for i in range(1, 30):
            csToken = self.get_csToken()
            data_xq = {
                'ah': '',  # 不变
                'fjm': 'J20',  # 不变
                'gglx': 'sdgg',  # 不变
                'xszt': '',  # 不变
                'ktzsfg': '',  # 不变
                'sjy': '',  # 不变
                'pagenumber': i,  # 当前页码数，可以遍历
                'dir': 'down',  # 往下是down王上是up
                'csToken': csToken,  # 要变，主要问题就是要找出这个是从哪里来的：是另一个post 请求来的，而且是随机的
                'token_key': '1808031025560986249',  # 不变
            }
            headers_xq = {
                'Host': 'sglccourts.gov.cn',
                'Connection': 'keep-alive',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Origin': 'http://sglccourts.gov.cn',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer': 'http://sglccourts.gov.cn/web/search?action=gotoggxxcx&gglx=sdgg&flag=first',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cookie': '__I18N_LOCALE__=zh_CN; 1533200178699=0E3F30963AA985FDD47CC7D06AF32BEB; JSESSIONID=B8E9023927AB3E6B164F240CCB28F865; 1533263029944=8BB99ED49F7D8955BD10978A0AE37ED6; 1533263137528=48BF5AD62D1E436EDD078DF43D05BD44; 1533263154792=8FBFD56BCD52AA0CA2A53ACC7FF3F99D; 1808031025560986249={}'.format(
                    csToken)
            }
            self.crawl(self.url_xq + '#{}'.format(i), callback=self.detail_page, method='POST', data=data_xq,
                       headers=headers_xq, save={'page': i})

    def detail_page(self, response):
        page = response.save['page']
        print(response.text)
        result_load = json.loads(response.text).get('ggList', '')
        for x in result_load:
            defendant = x.get('SSDR', '')
            print(defendant)
            case_no = x.get('AH', '')
            print(case_no)
            ann_date = x.get('UPDATETIME', '')
            print(ann_date)
            announcer = x.get('FYMC', '')
            print(announcer)
            ann_content = str(x)
            ann_html = str(x)
            print(ann_html)
            ann_type = '送达公告'
            content_url = 'http://sglccourts.gov.cn/web/search?action=gotoggxxcx#{}'.format(page)
            pdf_url = ''
            yield {
                'id': '',
                '_id_': '',
                'ann_type': ann_type,
                'announcer': announcer,
                'defendant': defendant,
                'ann_date': ann_date,
                'ann_content': ann_content,
                'ann_html': ann_html,
                'content_url': content_url,
                'pdf_url': pdf_url,
                'case_no': case_no,
                'source': '韶关中级人民法院',
            }

