#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/8/2 19:14
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
            'Host': 'www.hkfy.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
        }

    @every(minutes=24 * 60)
    def on_start(self):
        for i in range(1, 22):
            url = 'http://www.hkfy.gov.cn/a/shenpanxinxi/songdagonggao/list_65_{}.html'.format(i)
            self.crawl(url, callback=self.index_page, headers=self.headers)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):

        cookies = response.cookies

        urls = []
        times = []
        for each in response.doc('div.articleList div.bd ul li a[href]').items():
            urls.append(each.attr['href'])
        print(urls)
        for each in response.doc('div.articleList div.bd ul li span').items():
            times.append(each.text())
        if len(urls) == len(times):
            for i in range(len(urls)):
                self.crawl(urls[i], callback=self.detail_page, save={'ann_date': times[i]},cookies=cookies)

    @config(priority=2)
    def detail_page(self, response):
        ann_date = response.save['ann_date'] + 'T00:00:00+08:00'
        # print(ann_date)
        ann_type = '送达公告'

        ann_content = response.doc('div.articleList').text()
        ann_content = re.compile(r'(.*?)[【\[]打印[】\]]', re.S).findall(ann_content)
        if ann_content:
            ann_content = ann_content[0]
        else:
            ann_content = response.doc('div.articleList').text()
        print(1111, ann_content)
        print(type(ann_content))
        try:
            case_no = re.compile(r'[(（]201\d[）)].*?[书号]', re.S).findall(ann_content)[0]
        except:
            case_no = ''
        print(case_no, 222222)
        # print(ann_content)
        ann_content_list = ann_content.split('\n')
        ann_content_list = [x for x in ann_content_list if x != '']
        print(ann_content_list)
        defendant = ''
        announcer = ''

        for x in ann_content_list:
            if x.replace(' ', '').replace('\u3000', '').replace('\xa0', '')[-1] in [':', '：']:
                defendant = str(x[:-1].split('、'))
            if x.replace(' ', '').replace('\u3000', '').replace('\xa0', '')[-2:] == '法院':
                announcer = x
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
            'announcer': announcer,
            'defendant': defendant,
            'ann_date': ann_date,
            'ann_content': ann_content,
            'ann_html': ann_html,
            'content_url': content_url,
            'pdf_url': pdf_url,
            'case_no': case_no,
            'source': '海口法院网',
        }

