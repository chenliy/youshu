#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/31 16:46
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

from pyspider.libs.base_handler import *
import re


class Handler(BaseHandler):
    crawl_config = {
        'itag': 'v7.27',
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
            'Host': 'cczy.jlsfy.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'}

    @every(minutes=24 * 60)
    def on_start(self):
        for i in range(1, 3293):
            url = 'http://cczy.jlsfy.gov.cn/jxjsajgs/index_{}.jhtml'.format(i)
            self.crawl(url, headers=self.headers, callback=self.index_page)
        for i in range(1, 530):
            url = 'http://cczy.jlsfy.gov.cn/jxjsktgg/index_{}.jhtml'.format(i)
            self.crawl(url, headers=self.headers, callback=self.index_page)
        for i in range(1, 775):
            url = 'http://cczy.jlsfy.gov.cn/jxjsjyspdjg/index_{}.jhtml'.format(i)
            self.crawl(url, headers=self.headers, callback=self.index_page)
            #####
            # http://jxjs.court.gov.cn/打不开，这里感觉信息挺多的

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):

        cookies = response.cookies
        print(1)
        urls = []
        titles = []
        for each in response.doc('ul.organList a[href]').items():
            print(each.attr['href'])
            if 'index' not in each.attr['href']:
                urls.append(each.attr['href'])
                titles.append(each.text)
        times = []
        for each in response.doc('ul.organList div.date').items():
            times.append(each.text())
        print(len(times))
        print(len(urls))
        if len(urls) == len(times) == len(titles):
            for i in range(len(urls)):
                self.crawl(urls[i], callback=self.detail_page, save={'title': titles[i], 'ann_date': times[i]},
                           cookies=cookies)

    @config(priority=2)
    def detail_page(self, response):
        ann_date = response.save['ann_date']
        ann_type = '减刑假释'
        announcer = '长春市中级人民法院'

        ann_content = response.doc('div.page p.cjk').text().replace('\n', '').replace(' ', '').replace('\u3000',
                                                                                                       '').replace(
            '\xa0', '')
        print(ann_content)
        print(type(ann_content))
        try:
            case_no = re.compile(r'[(（]201\d[）)].*?号', re.S).findall(ann_content)[0]
        except:
            case_no = ''
        print(case_no, 1)
        # print(ann_content)
        ann_content_list = ann_content.split('\n')
        ann_content_list = [x for x in ann_content_list if x != '']
        print(ann_content_list)
        defendant = ''

        for x in ann_content_list:
            try:
                result = re.compile(r'罪犯(.*?)[，,。:：.]', re.S).findall(x)
                if result:
                    defendant = str(result[0].split('、'))
                    break
            except:
                continue

        # print(defendant)
        # print(announcer)
        content_url = response.url
        # print(content_url)
        ann_html = response.doc('div.page p.cjk').text().replace('\n', '').replace(' ', '').replace('\u3000',
                                                                                                    '').replace('\xa0',
                                                                                                                '')
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
            'source': '长春市中级人民法院司法公开网',
        }