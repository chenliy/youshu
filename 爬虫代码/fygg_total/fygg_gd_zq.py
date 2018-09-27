#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/30 16:53
# Project:
# @Author: ZQJ
# @Email : zihe@yscredit.com
from pyspider.libs.base_handler import *
from lxml import etree
import re


class Handler(BaseHandler):
    crawl_config = {
        'itag': 'v6.5',
        'time_out': 4000,
        # 'proxy': 'H14LXDJ6O07CAFDP:150D24D434AC09EE@proxy.abuyun.com:9010',
    }

    retry_delay = {
        0: 60,
        1: 60 * 5,
        2: 60 * 10,
        3: 60 * 15,
        4: 60 * 20,
        5: 60 * 25,
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
    @config(age=60 * 60)
    def on_start(self):
        url = 'http://zqzyssfw.gdzqfy.gov.cn/zqzy/front/ggxxList?ah=&fjm=JE0&gglx=sd&xszt=splc&pagenumber=2&dir=up&cs_token_flag=1&cs_token=21a2b8d642f845738e119bf21e63da63'
        self.crawl(url, callback=self.get_page)

    @config(age=60 * 60)
    def get_page(self, response):
        html = response.etree
        last_page = html.xpath('//div[@class="left"]//text()')
        all_page = int(re.findall(r'共(\d+)页', ''.join(last_page))[0]) + 1
        for i in range(1, 51):  # all_page
            url = 'http://zqzyssfw.gdzqfy.gov.cn/zqzy/front/ggxxList?ah=&fjm=JE0&gglx=sd&xszt=splc&pagenumber=' + str(
                i) + '&dir=up&cs_token_flag=1&cs_token=21a2b8d642f845738e119bf21e63da63'
            self.crawl(url, callback=self.index_page)

    @config(age=60 * 60)
    def index_page(self, response):
        try:
            html = response.etree
            table = html.xpath('//div[@class="doclist"]/table/tr')
            key = table[0].xpath('.//text()')
            key = list(map(lambda x: re.sub(r'\s', '', x), key))
            key = list(filter(lambda x: len(x) > 0, key))

            for each in table[1:]:
                case = each.xpath('.//text()')
                case = list(map(lambda x: re.sub(r'\s', '', x), case))
                case = list(filter(lambda x: len(x) > 0, case))
                print(case)

                ann_content = re.sub(r'[\{\}\']', '', str(dict(zip(key[1:], case[1:]))))
                case_on = case[1]
                ann_date = case[3] + 'T00:00:00+08:00'
                ann_html = etree.tounicode(each)
                defendant = case[5]

                yield {
                    'ann_type': '送达公告',
                    'announcer': '肇庆市中级人民法院',
                    'defendant': str(defendant),
                    'case_no': str(case_on),
                    'ann_content': str(ann_content),
                    'ann_date': str(ann_date),
                    'content_url': str(response.url),
                    'ann_html': str(ann_html),
                    'pdf_url': '',
                    'source': '肇庆市中级人民法院网上诉讼平台',
                    'id': '',
                    '_id_': ''
                }
        except Exception as e:
            print(e)