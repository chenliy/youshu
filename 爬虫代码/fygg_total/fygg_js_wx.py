# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/27 10:42
# Project:
# @Author: ZQJ
# @Email : zihe@yscredit.com

from pyspider.libs.base_handler import *
from lxml import etree
import re
from datetime import datetime


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
        'headers': headers,
        'itag': 'v5.25',
        'time_out': 4000
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
        url = 'http://wxzy.chinacourt.org/public/more.php?p=1&LocationID=1701000000&sub='
        self.crawl(url, callback=self.index_page)

    @config(age=60 * 60)
    def index_page(self, response):
        html = response.etree
        lists = html.xpath('//td[@class="xihei_141"]/table/tr')
        for each in lists[:-1]:
            href = each.xpath('td[@class="td_line"]/a/@href')[0]
            date = each.xpath('td[@class="td_time"]/text()')[0]
            url = 'http://wxzy.chinacourt.org' + href
            self.crawl(url, callback=self.detail_page, save={'date': date, })

        next_page = html.xpath('//td[@class="td_pagebar"]/a[last()]/@href')
        if next_page:
            next_url = 'http://wxzy.chinacourt.org' + next_page[0]
            self.crawl(next_url, callback=self.index_page)

    @config(priority=2)
    def detail_page(self, response):
        try:
            html = response.etree
            artical = html.xpath('//span[@class="detail_content"]//text()')
            ann_html = etree.tounicode(html.xpath('//span[@class="detail_content"]')[0])
            content = re.sub(r'\s|二$', '', ''.join(artical))
            ann_content = content
            # print(ann_content)


            case_on_list = re.findall(r'[(（][1１２2].{3}[）)].{0,8}[刑民行赔执访认送调管脏移引惩保].{2,18}?号', ann_content)
            if len(case_on_list) > 0:
                case_on = case_on_list[0]
            else:
                case_on = ''

            date = re.sub(r'[\(（）\)]', '', response.save['date'])
            ann_date = date + 'T00:00:00+08:00'

            # defendant = re.findall(r'号(.*?)[：:]',ann_content)[0].replace('、',',')
            defendant_l = html.xpath('//p[@align="center"]//text()')[0]

            defendant = re.findall(r'[-](.*?)$', defendant_l)
            if defendant:
                yield {
                    'ann_type': '送达公告',
                    'announcer': '无锡市中级人民法院',
                    'defendant': str(defendant[0]),
                    'case_no': str(case_on),
                    'ann_content': str(ann_content),
                    'ann_date': str(ann_date),
                    'content_url': str(response.url),
                    'ann_html': str(ann_html),
                    'pdf_url': '',
                    'source': '无锡市中级人民法院',
                    'id': '',
                    '_id_': ''}
        except Exception as e:
            print(e)

