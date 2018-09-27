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
        'itag': 'v1.1.6',
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
        url = 'http://www.qzcourt.gov.cn/News/sdggg/Index_1.html'
        self.crawl(url, callback=self.get_page)

    @config(age=60 * 60)
    def get_page(self, response):
        html = response.etree
        last_page = html.xpath('//div[@id="PageContent"]/a[last()-1]/text()')[0]
        for i in range(1, int(last_page) + 1):
            url = 'http://www.qzcourt.gov.cn/News/sdggg/Index_' + str(i) + '.html'
            self.crawl(url, callback=self.index_page)

    @config(age=60 * 60)
    def index_page(self, response):
        html = response.etree
        table = html.xpath('//table[@class="ltable"]/tr')
        for each in table:
            row = each.xpath('.//text()')
            row = list(map(lambda x: re.sub(r'\s', '', x), row))
            row = list(filter(lambda x: len(x) > 0, row))
            print(row)
            href = each.xpath('./td[3]/a/@href')
            url = 'http://www.qzcourt.gov.cn/News/sdggg/' + href[0]
            self.crawl(url, callback=self.detail_page, save={'row': row})

    @config(priority=2)
    def detail_page(self, response):
        try:
            html = response.etree
            content = ''.join(html.xpath('//div[@class="newtext"]//text()'))
            ann_content = re.sub(r'\s', '', content)
            row = response.save['row']
            ann_type = '送达公告'
            announcer = '泉州市中级人民法院'
            case_on = ''
            ann_date = row[-1] + 'T00:00:00+08:00'
            content_url = response.url
            ann_html = etree.tounicode(html.xpath('//div[@class="newtext"]')[0])
            pdf_url = ''
            source = '泉州市中级人民法院'
            defendant = row[2].replace('原告：', '').replace('被告：', ',').replace('、', ',')

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



