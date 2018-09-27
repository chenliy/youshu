#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-12-12 10:56:00
# Project: FYGG_GZ_ZS


from pyspider.libs.base_handler import *
from lxml import etree
from datetime import datetime
import re
import string
import hashlib
import json


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
        'time_out': 4000
    }

    # MD5加密函数
    def get_md5(self, s):
        """get md5 value
        Args
            s: a bytes, can be None
        Returns
            h.hexdigest(): md5(s) value, 32 bit.
        """
        if isinstance(s, str):
            s = bytes(s, encoding='utf-8')
        if s:
            h = hashlib.md5()
            h.update(s)
            return h.hexdigest()
        else:
            return ''

    # 对中文年份进行处理

    def parse_time(self, t):
        t = list(t)
        d = {
            '零': '0',
            '一': '1',
            '二': '2',
            '三': '3',
            '四': '4',
            '五': '5',
            'O': '0',
            '六': '6',
            '七': '7',
            '八': '8',
            '九': '9',
            '○': '0',
            'Ｏ': '0',
            '〇': '0',
            '年': '-',
            '月': '-',
            '日': '-',
            '元': '1'
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

    # 进行xpath封装
    def xml_xpath(self, response, choose):

        if choose == 1:
            return etree.HTML(response.content.decode('gbk', 'ignore'))
        else:
            return etree.HTML(response.text)

    @every(minutes=24 * 60)
    def on_start(self):
        url = 'http://zsfy.zsnews.cn/Article/index/id/7431.html'
        self.crawl(url, callback=self.index_page)

    @config(age=12 * 60 * 60)
    def index_page(self, response):
        # /html/body/center/table/tbody/tr/td[1]/table
        html = self.xml_xpath(response, 0)
        info_content = html.xpath('//div[@class="ArticleList"]/ul/li')
        for list in info_content:
            href = list.xpath('a/@href')[0]
            url = "http://zsfy.zsnews.cn" + href

            title = list.xpath('a/@title')[0]
            case_no = re.findall(r'(.*?号)', title)[0]

            # print(url,case_no)
            self.crawl(url, callback=self.detail_page, save={'case_no': case_no})

            # 翻页处理
        next_page = html.xpath('//div[@class="PageNav page"]/span/a[@class="next"]/@href')

        if len(next_page) > 0:
            org_url = "http://zsfy.zsnews.cn" + next_page[0]
            print(org_url)
            self.crawl(org_url, callback=self.index_page)
            # 详情页处理

    @config(priority=2)
    def detail_page(self, response):
        _id = ''
        _id_ = ''
        ann_type = '送达公告'
        announcer = '中山市中级人民法院'
        defendant = ''
        defendant_origin = ''
        ann_date = ''
        ann_content = ''
        ann_html = ''
        content_url = response.url
        pdf_url = ''
        case_no = ''
        source = '中山市中级人民法院'
        try:
            html = self.xml_xpath(response, 0)
            info_content = html.xpath('//td[@id="ArticleContent"]//text()')
            print(info_content)
            ann_html = etree.tounicode(html.xpath('//td[@id="ArticleContent"]')[0])
            print(ann_html)
            content_p = ''.join(info_content).replace('\xa0', '')
            content_p = content_p.replace('\r\n', '')
            ann_content = ''.join(content_p.split())
            print(ann_content)
            ann_date = re.findall(r'(.{4}[年].{1,2}[月].{1,3}[日号])', ann_content)[-1]
            print(ann_date)
            ann_date = self.parse_time(ann_date)
            print(ann_date)
            defendant_origin_list = re.findall(r'[号](.*?)[：:]', ann_content)[0]
            if '上诉人' in defendant_origin_list:
                defendant_origin_list = re.findall(r'上诉人(.*?)[：:]', ann_content)[0]
            if '、' in defendant_origin_list:
                defendants = defendant_origin_list.split('、')
            elif ',' in defendant_origin_list:
                defendants = defendant_origin_list.split(',')
            else:
                defendants = [defendant_origin_list]
            print(defendant_origin_list)
            case_no = str(response.save['case_no'])
            yield {
                "ann_type": ann_type,
                "announcer": announcer,
                "case_no": case_no,
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