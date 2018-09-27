#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/30 16:53
# Project:
# @Author: ZQJ
# @Email : zihe@yscredit.com

from pyspider.libs.base_handler import *
from lxml import etree
import re
from datetime import datetime


class Handler(BaseHandler):
    crawl_config = {
        'itag': 'v6.14',
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
    def on_start(self):
        url = 'http://nbfy.cnool.net/shared/articleList?page=1&type=3'
        self.crawl(url, callback=self.index_page)

    @config(age=12 * 60 * 60)
    def index_page(self, response):

        html = response.etree
        lists = html.xpath('//div[@class="item nopic"]')
        for each in lists:
            href = each.xpath('.//div[@class="caption"]/a[1]/@href')[0]
            title = each.xpath('.//div[@class="caption"]/a[2]/@title')[0]
            url = 'http://nbfy.cnool.net' + href
            self.crawl(url, callback=self.detail_page, save={'title': title})
        try:
            i = int(re.findall(r'page=(\d+)&', response.url)[0])
            i += 1
            next_url = 'http://nbfy.cnool.net/shared/articleList?page=' + str(i) + '&type=3'
            self.crawl(next_url, callback=self.index_page, )
        except Exception as e:
            print(e)
            print(i)

    @config(priority=2)
    def detail_page(self, response):
        try:
            html = response.etree
            content = html.xpath('//div[@class="content"]//text()')
            ann_html = etree.tounicode(html.xpath('//div[@class="content"]')[0])

            ann_content = re.sub(r'\s', '', ''.join(content))
            announcer = response.save['title']
            print(ann_content)

            defendant_l = re.findall(r'号(.{1,30})[:：]', ann_content)[0]
            if '(' or '（' in defendant_l:
                defendant = re.sub(r'[(（].*?[)）]', '', defendant_l)
            else:
                defendant = defendant_l[0]

            case_on_list = re.findall(r'[(（][1１２2].{3}[）)].{0,8}[刑民行赔执访认送调管脏移引惩保].{2,18}?号', ann_content)
            if len(case_on_list) > 0:
                case_on = case_on_list[0]
            else:
                case_on = ''

            date = re.findall(r'(.{4}年.{1,2}月.{1,3}日)', ann_content)[-1]
            print(date)
            ann_date = self.parse_time(date)
            print(ann_date)

            yield {
                'ann_type': '送达公告',
                'announcer': str(announcer),
                'defendant': str(defendant),
                'case_no': str(case_on),
                'ann_content': str(ann_content),
                'ann_date': str(ann_date),
                'content_url': str(response.url),
                'ann_html': str(ann_html),
                'pdf_url': '',
                'source': '宁波法院',
                'id': '',
                '_id_': ''

            }
        except Exception as e:
            print('AN ERROR :', e)

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
