#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/30 16:53
# Project:
# @Author: ZQJ
# @Email : zihe@yscredit.com

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
        'itag': 'v5.25',
        'headers': headers,
        'time_out': 4000,

    }

    # 对中文年份进行处理
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
    @config(age=60 * 60)
    def xml_xpath(self, response, choose):

        if choose == 1:
            return etree.HTML(response.content.decode('gbk', 'ignore'))
        else:
            return etree.HTML(response.text)

    @every(minutes=24 * 60)
    @config(age=60 * 60)
    def on_start(self):
        url = 'http://www.swzy.gov.cn/newslist.aspx?MenuId=02020402'
        self.crawl(url, callback=self.index_page)

    @config(age=60 * 60)
    def index_page(self, response):

        html = self.xml_xpath(response, 0)
        info_content = html.xpath('//ul[@class="mlist"]/li')
        print(info_content)
        for list in info_content:
            href = list.xpath('a/@href')[0]
            org_url = "http://www.swzy.gov.cn" + href
            # 进入详情页面
            # org_url='http://www.swzy.gov.cn/newsdetail.aspx?MenuId=02020402&id=1333'
            print(org_url)
            self.crawl(org_url, callback=self.detail_page)

        # 翻页处理..
        next_page = html.xpath('//div[@class="pages"]/a/@href')[-2]
        print(next_page)
        if "javascript:void(0)" != next_page:
            next_url = "http://www.swzy.gov.cn/newslist.aspx" + next_page
            print(next_url)

            self.crawl(next_url, callback=self.index_page)

    # 详情页处理
    @config(priority=2)
    @config(age=60 * 60)
    def detail_page(self, response):

        # 初始化字段
        _id = ''
        ann_type = '送达公告'
        announcer = '汕尾市中级人民法院'
        defendant = ''
        defendant_origin = ''
        ann_date = ''
        ann_content = ''
        ann_html = ''
        content_url = response.url
        pdf_url = ''
        case_no = ''
        source = '汕尾市中级人民法院'
        print("*******")
        try:
            html = self.xml_xpath(response, 0)
            content = html.xpath('//div[@class="mcondiv2"]')[0]
            ann_html = etree.tounicode(content)

            title = content.xpath('div[@class="decontitle"]/text()')[0]
            print(title)
            if '公告' in title:

                check = re.findall(r'([（\(][0-9]{4}[）\)].*?号)', title)

            else:
                check = re.findall(r'(.*号)', title)
            if len(check) > 0:

                case_no = check[0]
            else:
                case_no = html.xpath('//div[@align="right"]/span/text()')

            print(title, case_no)
            time = html.xpath('//div[@class="deconby"]/text()')[0].split()[-1]
            print(time)
            date_time = time.split('：')[-1]
            print(date_time)

            content_all = html.xpath('//div[@class="decon"]//text()')
            # print(content_all)
            content_p = ''.join(content_all).replace('\xa0', '')
            content_p = content_p.replace('\r\n', '')
            ann_content = ''.join(content_p.split())

            dates = re.findall(r'(.{4}[-年\.].{1,2}[-月\.].{1,3}[日号\.\s])', ann_content)

            print(len(dates))
            if len(dates) > 0:
                print("*********")
                ann_date = self.parse_time(dates[-1])
            else:

                # ann_date = datetime.strptime(date_time, "%Y-%m-%d").strftime('%Y-%m-%dT00:00:00+08:00')
                date_time = date_time.replace('.', '-')
                ann_date = date_time + "T00:00:00+08:00"
            defendant_origin_list = re.findall(r'号(.*)[：:]', ann_content)[0]

            print(defendant_origin_list)
            if '之一' in defendant_origin_list:
                defendant_origin_list = re.findall(r'之一(.*?)[：:]', ann_content)[0]
            if '、' in defendant_origin_list:
                defendants = defendant_origin_list.split('、')
            elif ',' in defendant_origin_list:
                defendants = defendant_origin_list.split(',')
            else:
                defendants = [defendant_origin_list]
            print(defendant_origin_list)
            case_no = re.findall(r'(（[0-9]{4}）.*?号)', ann_content)
            if case_no:
                case_no = case_no[0]
            if defendant_origin_list not in '本院在执行':
                yield {
                    "ann_type": ann_type,
                    "announcer": announcer,
                    "case_no": str(case_no),
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