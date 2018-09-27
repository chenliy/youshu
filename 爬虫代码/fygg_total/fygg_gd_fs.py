# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/27 10:42
# Project:法院公告-广东-佛山
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
        1: 60 * 5,
        2: 60 * 10,
        3: 60 * 15,
        4: 60 * 20,
        5: 60 * 25,
    }
    crawl_config = {
        'itag': 'v7.7',
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
        self.crawl('http://www.fszjfy.gov.cn/pub/court_7/sifagongkai/fayuangonggao/songda/index.html',
                   callback=self.get_page)

    @config(age=60 * 60)
    def get_page(self, response):
        pages = re.findall(r'createPageHTML\((.*?),', response.text)[0]
        print(pages)
        try:
            for i in range(1, int(pages) + 1):
                next_url = 'http://www.fszjfy.gov.cn/pub/court_7/sifagongkai/fayuangonggao/songda/index_' + str(
                    i) + '.html'
                # print(next_url)
                self.crawl(next_url, callback=self.index_page)
        except Exception as e:
            print(e)
            print('爬虫翻页出错')

    @config(age=60 * 60)
    def index_page(self, response):

        html = etree.HTML(response.text)
        lists = html.xpath('//td[@align="center"]/table[2]/tr')
        for each in lists[1:]:
            href_list = each.xpath('td/a/@href')
            href = re.sub(r'^.', '', href_list[0])
            url = 'http://www.fszjfy.gov.cn/pub/court_7/sifagongkai/fayuangonggao/songda' + href
            self.crawl(url, callback=self.detail_page)

    @catch_status_code_error
    @config(priority=2)
    def detail_page(self, response):
        if response.status_code == 200:
            try:
                html = etree.HTML(response.content.decode('utf-8', 'ignore'))

                ann_html = etree.tounicode(html.xpath('//td[@class="document position10"]')[0])
                content_all = html.xpath('//td[@class="document position10"]//text()')
                content = ('').join(content_all)
                content_all = re.sub(r'\s', '', content)

                ann_content = re.findall(r'人民法院(.*日)', content_all)[0]
                print(ann_content)

                ann_type = '送达公告'
                announcer = '佛山市中级人民法院'
                source = '佛山市中级人民法院'
                content_url = response.url
                pdf_url = ''

                defendant_origin = re.findall(r'号(.*?)[：:]', ann_content)[0]
                defendant_origin = re.sub(r'^之.?', '', defendant_origin)
                if re.findall(r'([，。；])', defendant_origin):
                    print('可能出了问题，抛个未定义的error')
                    error
                print(defendant_origin)

                date = re.findall(r'(.{4}年.{1,2}月.{1,3}日)', ann_content)[-1]
                print(date)
                ann_date = self.parse_time(date)

                case_on = re.findall(r'[(（][1１２2].{3}[）)].{0,8}[刑民行赔执访认送调管脏移引惩保].{2,18}号', ann_content)[0]
                print(case_on)

                defendant = defendant_origin.split('、')
                print(
                    '"ann_type":{},"announcer":{},"case_no":{},"ann_content":{},"ann_date":{},"content_url":{}"ann_html":{}"pdf_url":{}"source":{}"defendant":{}'.format(
                        len(ann_type), len(announcer), len(case_on), len(ann_content), len(ann_date), len(content_url),
                        len(ann_html), len(pdf_url), len(source), len(defendant)))

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