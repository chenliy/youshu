#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/27 11:33
# Project:
# @Author: ZQJ
# @Email : zihe@yscredit.com


from pyspider.libs.base_handler import *
from lxml import etree
import re
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
        1: 60 * 1,
        2: 60 * 2,
        3: 60 * 3,
        4: 60 * 4,
        5: 60 * 5,
    }
    crawl_config = {
        'itag': 'v7.27',
        'headers': headers,
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

    @every(minutes=24 * 60)
    @config(age=60 * 60)
    def on_start(self):
        self.crawl('http://www.hshfy.sh.cn/shfy/gweb2017/sdgg_search.jsp?zd=splc', callback=self.get_page)

    @config(age=60 * 60)
    def get_page(self, response):

        html = etree.HTML(response.text)
        # pages = html.xpath('//div[@align="center"]/a/@href')[-1]
        # page_num = re.findall(r'(\d+)', pages)[0]
        for i in range(1, 50):  #
            data = {
                "pagesnum": i,
                "fbrqks": '',
                "fbrqjs": '',
                "fydm": '',
            }
            self.crawl('http://www.hshfy.sh.cn/shfy/gweb2017/sdgg_search.jsp?zd=splc#{}'.format(str(i)), method="POST",
                       data=data, callback=self.index_page)

    @config(age=60 * 60)
    def index_page(self, response):
        html = etree.HTML(response.text)
        lists = html.xpath('//div[@class="list_a"]/ul/li')

        for each in lists:
            date = each.xpath('span/text()')[0]
            ann_date = re.sub(r'[\[\]]', '', date)

            href = each.xpath('a/@href')[0]
            url = 'http://www.hshfy.sh.cn/shfy/gweb2017/' + href
            self.crawl(url, callback=self.detail_page, save={'ann_date': ann_date})

    @catch_status_code_error
    @config(priority=2)
    def detail_page(self, response):
        # print(response.text)
        if response.status_code == 200:
            try:
                html = etree.HTML(response.text)
                ann_html = etree.tounicode(html.xpath('//div[@class="nrtxt"]')[0])
                content_list = html.xpath('//div[@class="nrtxt"]//text()')
                # print(content_list)

                ann_type = '送达公告'
                announcer = content_list[-2]
                source = '上海市高级人民法院网'
                content_url = response.url
                pdf_url = ''

                content = ('').join(content_list)
                ann_content = re.sub(r'[\xa0\n\t\u3000\r]', '', content)

                namestr = ('').join(html.xpath('//div[@class="wby"]/text()')).replace('\n', '')
                defendant_origin = re.findall(r'——(.*[\u4e00-\u9fa5])', namestr)[0]

                if re.findall(r'[(执行)(送达)(通知书)]', defendant_origin):
                    print('无当事人或当事人有异')
                    error

                case_on_list = re.findall(r'[(（][1１２2].{3}[）)].{0,8}[刑民行赔执访认送调管脏移引惩保].{2,18}号', ann_content)
                if len(case_on_list) > 0:
                    case_on = case_on_list[0]
                else:
                    case_on = ''
                # print(case_on)

                date = response.save['ann_date']
                # print(date)
                ann_date = self.parse_time(date)

                defendant = defendant_origin.replace('、', ',')

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
                print(response.url, '该网站形式有异')

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
        try:
            t = re.findall(r'(.{4}[-年\.].{1,2}[-月\.].{1,3}?)[-上下日号\s]', t)[0]
            t = datetime.strptime(t, "%Y-%m-%d").strftime('%Y-%m-%dT00:00:00+08:00')
        except:
            t = datetime.strptime(t, "%Y-%m-%d").strftime('%Y-%m-%dT00:00:00+08:00')
        return t
