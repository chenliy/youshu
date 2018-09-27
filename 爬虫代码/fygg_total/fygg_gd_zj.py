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
    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }

    retry_delay = {
        0: 60,
        1: 60 * 5,
        2: 60 * 10,
        3: 60 * 15,
        4: 60 * 20,
        5: 60 * 25,
    }
    crawl_config = {
        'itag': 'v4.23',
        'headers': headers,
        'time_out': 4000,
        # 'proxy': 'H14LXDJ6O07CAFDP:150D24D434AC09EE@proxy.abuyun.com:9010'

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
                  {"name": "defendant", "type": "string"},
                  ]

    @every(minutes=24 * 60)
    @config(age=60 * 60)
    def on_start(self):
        url = 'http://www.zjcourt.gov.cn/zjzy/front/ggxxList/J80-splc-up-2-?gglx=sd#up'
        self.crawl(url, callback=self.get_page)

    @config(age=60 * 60)
    def get_page(self, response):
        html = response.etree
        all_data = html.xpath('//span[@class="pageleft"]/strong/text()')[0]
        all_page = int(all_data) // 10
        if all_page % 10 > 0:
            all_page += 1
        for i in range(1, all_page):
            if i == 1:
                url = 'http://www.zjcourt.gov.cn/zjzy/front/ggxxList/J80-splc-up-2-?gglx=sd#up'
            else:
                url = 'http://www.zjcourt.gov.cn/zjzy/front/ggxxList/J80-splc-down-' + str(i - 1) + '-?gglx=sd#up'
            self.crawl(url, callback=self.index_page)

    @config(age=60 * 60)
    def index_page(self, response):
        html = response.etree
        lists = html.xpath('//div[@class="list"]/ul/a')
        for each in lists:
            case_on = each.xpath('./li/text()')[0]
            href = each.xpath('./@href')[0]
            url = 'http://www.zjcourt.gov.cn' + href
            self.crawl(url, callback=self.detail_page, save={'case_on': case_on})

    @config(priority=2)
    def detail_page(self, response):
        try:
            html = response.etree
            table_list = html.xpath('//div[@class="bg"]/div[starts-with(@class,"item")]//text()')
            table_list = list(map(lambda x: re.sub(r'\s', '', x), table_list))
            table_list = list(filter(lambda x: len(x) > 0, table_list))
            values = table_list[1::2]
            i = 2
            while i < len(table_list):
                table_list.insert(i, ',')
                i += 3
            print(table_list)

            ann_type = '送达公告'
            announcer = '湛江市中级人民法院'
            ann_content = ''.join(table_list)
            ann_date = values[1] + 'T00:00:00+08:00'
            content_url = response.url
            ann_html = etree.tounicode(html.xpath('//div[@class="bg"]/div[starts-with(@class,"item")]')[0])
            pdf_url = ''
            source = '湛江法院诉讼服务中心'
            defendant = values[0]
            case_on = response.save['case_on']

            yield {
                "ann_type": ann_type,
                "announcer": announcer,
                "case_no": case_on,
                "ann_content": ann_content,
                "ann_date": str(ann_date),
                "content_url": content_url,
                "ann_html": str(ann_html),
                "pdf_url": pdf_url,
                "source": source,
                "defendant": str(defendant),
                "id": '',
                "_id_": ''
            }
        except Exception as e:
            print(e)