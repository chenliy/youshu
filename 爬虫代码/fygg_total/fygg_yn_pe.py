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
import logging

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

    # 时间处理函数
    def get_date(self, court_time):
        if not court_time:
            return court_time
        court_date = re.findall(r'(.{4}[-年\.].{1,2}[-月\.].{1,3}?)[上下日号\s]', court_time)[0] if re.findall(
            r'(.{4}[-年\.].{1,2}[-月\.].{1,3}?)[上下日号\s]', court_time) else ''
        logging.warning(court_date)
        special_str = '〇一二三四五六七八九十元'
        pos = 0
        while 1 and pos < len(court_date):
            if court_date[pos] in special_str:
                return court_date
            else:
                pos += 1
        if '-' in court_date:
            court_date = datetime.strptime(court_date, "%Y-%m-%d").strftime('%Y-%m-%dT00:00:00+08:00')
        elif '.' in court_date:
            court_date = datetime.strptime(court_date, "%Y.%m.%d").strftime('%Y-%m-%dT00:00:00+08:00')
        elif '年' in court_date:
            court_date = datetime.strptime(court_date, "%Y年%m月%d").strftime('%Y-%m-%dT00:00:00+08:00')
        return court_date

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
        url = 'http://pezy.ynfy.gov.cn/qtgg/index.jhtml'
        self.crawl(url, callback=self.index_page)

    @config(age=12 * 60 * 60)
    @config(age=60 * 60)
    def index_page(self, response):
        html = self.xml_xpath(response, 0)
        info_list = html.xpath('//div[@class="c1-body"]/li')
        print(info_list)
        for list in info_list:
            org_url = list.xpath('a/@href')[0]
            print(org_url)
            title = list.xpath('a/@title')[0]
            print(title)
            check = re.findall(r'(（.{4}）.*?号)', title)
            if len(check) > 0:
                print("****")
                case_no = check[0]
                print(case_no)

                self.crawl(org_url, callback=self.detail_page, save={'case_no': case_no})
                # 翻页处理
        next_page = html.xpath('//div[@class="turn_page"]/p/a/@href')[-1]
        url = "http://pezy.ynfy.gov.cn/qtgg/" + next_page
        print(url)
        #
        self.crawl(url, callback=self.index_page)

    @config(priority=2)
    def detail_page(self, response):
        # 初始化字段
        _id = ''
        _id_ = ''
        ann_type = '送达公告'
        announcer = '普洱市中级人民法院'
        defendant = ''
        defendant_origin = ''
        ann_date = ''
        ann_content = ''
        ann_html = ''
        content_url = response.url
        pdf_url = ''
        case_no = ''
        source = '普洱市中级人民法院'

        try:
            html = self.xml_xpath(response, 0)
            content_text = html.xpath('//div[@class="sswy_article_m"]//text()')

            ann_html = etree.tounicode(html.xpath('//div[@class="sswy_article_m"]')[0])
            # print(ann_html)
            content_p = ''.join(content_text).replace('\xa0', '')
            content_p = content_p.replace('\r\n', '')
            ann_content = ''.join(content_p.split())

            ann_date = re.findall(r'(.{4}[年].{1,2}[月].{1,3}[日号])', ann_content)[-1]

            ann_date = self.parse_time(ann_date)

            text = ann_content.replace('本院', '：')
            text = text.split('：')[0] + ":"
            case = re.findall(r'(（.{4}）.*?)号', text)
            print(len(case))
            print(text)
            if len(case) > 0:
                print("*******")
                defendant_origin_list = re.findall(r'号(.*?):', text)[0]
                # print(defendant_origin_list)
            elif '公告' in text:
                defendant_origin_list = re.findall(r'公告(.*?):', text)[0]
                # print(defendant_origin_list)

            else:
                defendant_origin_list = re.findall(r'(.*?):', text)[0]

            print(defendant_origin_list)

            if '上诉人' in defendant_origin_list:
                defendant_origin_list = re.findall(r'上诉人(.*?)[：:]', defendant_origin_list)[0]
            if '、' in defendant_origin_list:
                defendants = defendant_origin_list.split('、')
            elif ',' in defendant_origin_list:
                defendants = defendant_origin_list.split(',')
            else:
                defendants = [defendant_origin_list]

            case_no = str(response.save['case_no'])
            # print(case_no)
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
