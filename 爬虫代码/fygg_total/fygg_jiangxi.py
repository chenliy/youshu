# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/27 10:42
# Project:
# @Author: ZQJ
# @Email : zihe@yscredit.com

from pyspider.libs.base_handler import *
from lxml import etree
import re
import json
import hashlib
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
        'itag': 'v4.23',
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

        self.crawl('http://sd.dolawing.com/deli/DeliNotice/delinotice!getNoticeAjax.action', callback=self.index_page)

    @config(age= 60 * 60)
    def index_page(self, response):
        # 网站采用加载JSON得方式，以下解析JSON并获取相关字段
        jsons = json.loads(response.text)
        #print(jsons)

        lists = jsons['message']['result']
        for each in lists:
            case_on = each['caseCode']
            defendant_origin = each['peopleName']
            ann_date = each['publicTimeString']
            announcer = each['orgName']
            print(case_on, defendant_origin, ann_date)

            word = {
                'case_on': case_on,
                'defendant_origin': defendant_origin,
                'ann_date': ann_date,
                'announcer': announcer,
            }

            url_id = each['id']
            url = 'http://sd.dolawing.com/deli/web/delinoticeview!noticeView.action?id=' + str(url_id)
            self.crawl(url, callback=self.detail_page, save=word)
            # word.clear()

        # 翻页处理(隐患--一页死掉 之后的全没能打开)
        next_page = jsons['message']['nextPage']
        data = {
            "page.pageNo": next_page
        }
        self.crawl('http://sd.dolawing.com/deli/DeliNotice/delinotice!getNoticeAjax.action#{}'.format(str(next_page)),
                   method="POST", data=data, callback=self.index_page)

    @catch_status_code_error
    @config(priority=2)
    def detail_page(self, response):
        if response.status_code == 200:
            html = etree.HTML(response.text)

            # 正文以文本的形式放于源码中
            content_table = html.xpath('//div[@class="zw"]/script[@id="container"]//text()')[0]
            tree = etree.HTML(content_table)
            content_list = tree.xpath('//p//text()')

            ann_html = etree.tounicode(tree)

            content = ('').join(content_list).replace('\xa0', '')
            ann_content = re.sub(r'[\n\r\xa0\u3000\t]', '', content)
            #print(ann_content)

            ann_type = '送达公告'
            source = '江西法院司法文书送达网'
            content_url = response.url
            pdf_url = ''
            #print(response.save)
            case_on = response.save['case_on']
            defendant_origin = response.save['defendant_origin']
            announcer = response.save['announcer']
            date = response.save['ann_date']
            #print(date)
            ann_date = self.parse_time(date)

            defendant = defendant_origin.split('、')

            yield {
                    "ann_type": ann_type,
                    "announcer": announcer,
                    "case_no": case_on,
                    "ann_content": ann_content,
                    "ann_date": ann_date,
                    "content_url": content_url,
                    "ann_html": ann_html,
                    "pdf_url": pdf_url,
                    "source": source,
                    "defendant": str(defendant),
                    "id": '',
                    "_id_": ''
                }
    def parse_time(self, t):
        t = list(t)
        d = {'零': '0', '一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9',
             '○': '0', 'Ｏ': '0', '年': '-', '月': '-', '日': '-', '元': '1', '〇': '0','Ο':'0','０':'0',
             'О':'0','0':'0','O':'0','o':'0'
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












