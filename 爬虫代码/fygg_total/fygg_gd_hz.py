# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/27 10:42
# Project:法院公告-广东-惠州
# @Author: ZQJ
# @Email : zihe@yscredit.com
from pyspider.libs.base_handler import *
import re
from lxml import etree
from datetime import datetime
import hashlib


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
        'itag': 'v6.12',
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
        url = 'http://www.hzzy.gov.cn/web/list/1051-#start'
        self.crawl(url, callback=self.get_page)

    @config(age=60 * 60)
    def get_page(self, response):
        all_page = int(re.findall('共(\d+)页', response.text)[0]) + 1
        for i in range(1, all_page):
            url = 'http://www.hzzy.gov.cn/web/list/1051-?page=' + str(i)
            self.crawl(url, callback=self.index_page)

    @config(age=60 * 60)
    def index_page(self, response):
        html = etree.HTML(response.text)
        lists = html.xpath('//div[@class="titlelist"]/ul/li')
        for each in lists:
            href = each.xpath('a/@href')[0]
            title = each.xpath('./a/text()')[0]
            url = 'http://www.hzzy.gov.cn' + href
            self.crawl(url, callback=self.detail_page, save={'title': title})

    @catch_status_code_error
    @config(priority=2)
    def detail_page(self, response):
        if response.status_code == 200:
            try:
                html = etree.HTML(response.text)

                content_all = html.xpath('//div[@class="articlecontent"]//text()')
                ann_html = etree.tounicode(html.xpath('//div[@class="articlecontent"]')[0])
                content_str = ('').join(content_all)
                content = re.sub(r'[\n\r\t\xa0\u3000 ]', '', content_str)
                ann_content = content

                ann_type = '送达公告'
                announcer = '惠州市中级人民法院'
                source = '惠州市中级人民法院'
                content_url = response.url
                pdf_url = ''

                date = re.findall(r'(.{4}年.{1,2}月.{1,3}日)', ann_content)[-1]
                ann_date = self.parse_time(date)

                case_on_list = re.findall(r'[(（][1１２2].{3}[）)].{0,8}[刑民行赔执访认送调管脏移引惩保].{2,18}号', ann_content)
                if len(case_on_list) > 0:
                    case_on = case_on_list[0]
                else:
                    case_on = ''
                print(case_on)

                defendant = re.sub(r'[-———]', '$', response.save['title'].strip()).split('$')[-1].replace('、', ',')

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
                print(response.url, '该网页形式有异')

    def parse_time(self, t):
        t = list(t)
        d = {'零': '0', '一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9',
             '○': '0', 'Ｏ': '0', '年': '-', '月': '-', '日': '-', '元': '1', '〇': '0', 'Ο': '0', '０': '0',
             'О': '0', '0': '0', 'O': '0', 'o': '0'
             }
        for i in range(len(t)):
            if t[i] in d.keys():
                t[i] = d[t[i]]
        # 处理汉字为十的情况
        if '十' in t:
            for i in range(len(t)):
                if t[i] == '十':
                    if (i - 1) >= 0 and t[i - 1].isalnum():
                        t[i] = '0'
                    if (i + 1) < len(t) and t[i + 1].isalnum():
                        t[i] = '1'
                    if (i - 1) >= 0 and (i + 1) < len(t) and t[i - 1] == '-' and t[i + 1] == '-':
                        t[i] = '10'
                    if (i - 1) >= 0 and (i + 1) < len(t) and t[i - 1].isalnum() and t[i + 1].isalnum():
                        t[i] = ''
        t = ''.join(t)
        t = re.findall(r'(.{4}[-年\.].{1,2}[-月\.].{1,3}?)[-上下日号\s]', t)[0]
        t = datetime.strptime(t, "%Y-%m-%d").strftime('%Y-%m-%dT00:00:00+08:00')
        return t







