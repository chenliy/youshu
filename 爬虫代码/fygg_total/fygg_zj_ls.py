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
        'itag': 'v524',
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
        url = 'http://www.zjlscourt.com/lishui/splc/sdgg/index.html'
        self.crawl(url, callback=self.get_page)

    def get_page(self, response):
        all_page = re.findall('页次：(.*?)每页', response.text)[0]
        last_page = re.findall(r'/(\d)+&', all_page)[0]
        for i in range(1, int(last_page) + 1):
            if i == 1:
                url = response.url
            else:
                url = 'http://www.zjlscourt.com/lishui/splc/sdgg/index_' + str(i) + '.html'
            self.crawl(url, callback=self.index_page)

    @config(age=60 * 60)
    def index_page(self, response):
        html = response.etree
        lists = html.xpath('//table[@class="news_space"]//table//tr')
        for each in lists:
            href = each.xpath('./td/a/@href')[0]
            date = each.xpath('./td[@class="news_date"]/text()')[0]
            self.crawl(href, callback=self.detail_page, save={'date': date})

    @config(priority=2)
    def detail_page(self, response):
        try:
            html = response.etree
            content = html.xpath('//table[@class="news_space"]/tr[5]//text()')
            content = re.sub(r'\s', '', ''.join(content))
            print(content)

            ann_type = '送达公告'
            announcer = '丽水市中级人民法院'
            ann_content = content
            content_url = response.url
            pdf_url = ''
            source = '丽水市中级人民法院'
            ann_html = etree.tounicode(html.xpath('//table[@class="news_space"]/tr[5]')[0])

            case_on_list = re.findall(r'[(（][1１２2].{3}[）)].{0,8}[刑民行赔执访认送调管脏移引惩保].{2,18}号', ann_content)
            if len(case_on_list) > 0:
                case_on = case_on_list[0]
            else:
                case_on = ''

            ann_date = re.sub(r'\s', '', response.save['date']) + 'T00:00:00+08:00'

            defendant = re.findall(r'^(.*?)[：:]', ann_content)[0].replace('、', ',')

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

