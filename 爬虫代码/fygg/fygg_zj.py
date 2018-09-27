#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/8/3 10:08
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

from pyspider.libs.base_handler import *
import re


class Handler(BaseHandler):
    crawl_config = {
        'itag': 'v7.30',
        'time_out': 100000,
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

    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.zjcourt.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
        }

    @every(minutes=24 * 60)
    def on_start(self):
        # 32415条数据，每页10条
        for i in range(0, 3242):
            if i == 0:
                url = 'http://www.zjcourt.gov.cn/zjzy/front/ggxxList/J80-splc-?gglx=sd'
            else:
                url = 'http://www.zjcourt.gov.cn/zjzy/front/ggxxList/J80-splc-down-{}-?gglx=sd#up'.format(i)
            self.crawl(url, callback=self.index_page, headers=self.headers)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):

        # print(response.text)

        cookies = response.cookies

        urls = []
        times = []
        for each in response.doc('div.list ul a[href]').items():
            urls.append(each.attr['href'])

        for each in response.doc('div.list ul a li span.date').items():
            times.append(each.text())

        print(urls)
        print(times)
        if len(urls) == len(times):
            for i in range(len(urls)):
                self.crawl(urls[i], callback=self.detail_page, save={'ann_date': times[i]}, cookies=cookies)

    @config(priority=2)
    def detail_page(self, response):

        ann_date = response.save['ann_date'] + 'T00:00:00+08:00'

        # print(ann_date)
        ann_type = '送达公告'

        ann_content = response.doc('div.case').text()

        case_no = re.compile(r'([\(（]?\d{4}.*?\d号)').findall(ann_content)
        if case_no:
            case_no = case_no[0]
        # print(case_no)
        # print(1111, ann_content)
        # print(type(ann_content))

        # print(ann_content)
        ann_content_list = ann_content.split('\n')
        ann_content_list = [x for x in ann_content_list if x != '']
        print(ann_content_list)
        defendant = ''

        for i in range(len(ann_content_list)):
            if '受送达人' in ann_content_list[i]:
                defendant = ann_content_list[i + 1]
                break
        # print(defendant)
        # print(announcer)
        content_url = response.url
        # print(content_url)
        ann_html = ann_content
        # print(ann_html)
        pdf_url = ''

        yield {
            'id': '',
            '_id_': '',
            'ann_type': ann_type,
            'announcer': '湛江中级人民法院',
            'defendant': defendant,
            'ann_date': ann_date,
            'ann_content': ann_content,
            'ann_html': ann_html,
            'content_url': content_url,
            'pdf_url': pdf_url,
            'case_no': case_no,
            'source': '湛江法院诉讼服务中心',
        }

