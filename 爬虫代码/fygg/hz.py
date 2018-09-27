#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/27 19:46
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
                  {"name": "defendant", "type": "string"},
                  ]

    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'hangzhou.zjcourt.cn',
            'Referer': 'http://hangzhou.zjcourt.cn/col/col1218371/index.html',
            'Cookies': 'JSESSIONID=53F63C2143F4927A72A9D246D1B9A346; acw_tc=AQAAAOFs9iVtCQIA4zedt+sLReWzToys; SERVERID=e146d554a29ee4143047c903abfbc3da|1532912078|1532911850',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
        }

    @every(minutes=24 * 60)
    def on_start(self):
        # 三小页，一大页，目前是10页多一条数据，爬全量且不更新，写死：
        for i in range(1, 5):
            data = {
                'col': '1',
                'appid': '1',
                'webid': '1903',
                'path': '/',
                'columnid': '1218371',
                'sourceContentType': '1',
                'unitid': '3989778',
                'webname': '杭州市中级人民法院',
                'permissiontype': '0',
            }
            if i == 4:
                # 第四大页就一条数据
                url = 'http://hangzhou.zjcourt.cn/module/jpage/dataproxy.jsp?startrecord=181&endrecord=181&perpage=20'
            else:
                url = 'http://hangzhou.zjcourt.cn/module/jpage/dataproxy.jsp?startrecord={}&endrecord={}&perpage=20'.format(
                    i * 60 - 59, i * 60)

            self.crawl(url, headers=self.headers, data=data, method='POST', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        print(response.text)
        cases_no = re.compile(r'lank">(.*?[号告])</a>', re.S).findall(response.text)
        print(cases_no)
        times = re.compile(r'style="font-size:14px;">(.*?)</td></tr', re.S).findall(response.text)
        print(times)
        urls = re.compile(r'href=\'(.*?)\' class=', re.S).findall(response.text)
        print(urls)
        print(len(urls), len(times), len(cases_no))
        if len(times) == len(urls):
            for i in range(len(urls)):
                url = 'http://hangzhou.zjcourt.cn' + urls[i]
                self.crawl(url, callback=self.detail_page, headers=self.headers,
                           save={'case_no': cases_no[i], 'ann_date': times[i]})

    @config(priority=2)
    def detail_page(self, response):
        case_no = response.save['case_no']
        ann_date = response.save['ann_date']

        b = []
        for each in response.doc('td.bt_content_w div#zoom > *').items():
            if each.text().replace(' ', '').replace('\u3000', '').replace('\xa0', ''):
                b.append(each.text().replace(' ', '').replace('\u3000', '').replace('\xa0', ''))

        ann_content = str(b)
        for i in range(len(b)):
            if ':' in b[i] or '：' in b[i]:
                defendant = re.compile('(.*?)[:：]', re.S).findall(b[i])
                break

        defendant = defendant[0].split('、')
        ann_html = response.doc('td.bt_content_w div#zoom').text()

        yield {
            'id': '',
            '_id_': '',
            'ann_type': '送达公告',
            'announcer': '杭州市中级人民法院',
            'defendant': defendant,
            'ann_date': ann_date,
            'ann_content': ann_content,
            'ann_html': ann_html,
            'content_url': response.url,
            'pdf_url': '',
            'case_no': case_no,
            'source': '杭州市中级人民法院',
        }

