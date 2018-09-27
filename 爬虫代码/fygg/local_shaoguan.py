#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/8/4 10:36
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

from pyspider.libs.base_handler import *
import re
import requests
import json


class Handler(BaseHandler):
    crawl_config = {
        'itag': 'v7.30',
        # 'time_out': 100000,
        # 'proxy': 'H67U07LZ5DMU714P:91C4756816F315D4@http-pro.abuyun.com:9010'

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

    @every(minutes=24 * 60)
    def on_start(self):

        url_mm = 'http://sglccourts.gov.cn/common/getToKenTempPutCk'
        data_mm = {
            'tokenKey': '1808031025560986249'
        }
        headers_mm = {
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
        self.crawl(url_mm, method='POST', data=data_mm, callback=self.index_page, headers=headers_mm)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):

        csToken = eval(response.text).get("tokenVal", 'a689e58760f4465ea42d4560da6c046b')
        print(csToken)

        url_xq = 'http://sglccourts.gov.cn/web/search?action=gotoggxxcx'

        for i in range(1, 1230):
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

            self.crawl(url_xq + '#{}'.format(i), callback=self.detail_page, method='POST', data=data_xq,
                       headers=headers_xq, save={'page': i})

    @config(priority=2)
    def detail_page(self, response):

        page = response.save['page']
        print(response.text)
        result = json.loads(response.text).get('ggList', '')
        print(result)
        ann_type = '送达公告'
        for x in result:
            defendant = x.get('SSDR', '')
            case_no = x.get('AH', '')
            ann_date = x.get('UPDATETIME', '').split(' ')[0] + 'T00:00:00+08:00'
            announcer = x.get('FYMC', '')
            ann_content = str(x)
            ann_html = str(x)
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

