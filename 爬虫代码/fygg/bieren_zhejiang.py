#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/27 10:42
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-12-12 19:08:35
# Project: FYGG_YN_ZJFY

from pyspider.libs.base_handler import *
from lxml import etree
import re
import logging
from datetime import datetime
import hashlib
import json
import time
import requests


class Handler(BaseHandler):
    headers = {
        'Host': 'www.zjsfgkw.cn',
        'Origin': 'http://www.zjsfgkw.cn',
        'Referer': 'http://www.zjsfgkw.cn/Notice/NoticeSDList',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
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
        'itag': 'v68779',
        'headers': headers,
        'time_out': 8000
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

    # 时间处理函数
    def get_court_date(self, court_time):
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
            print("****")
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

    @every(minutes=24 * 60)
    @config(age=60 * 60)
    def on_start(self):
        url = 'http://www.zjsfgkw.cn/Notice/NoticeSDSearch'

        data = {
            'pageno': '1',
            'pagesize': '10'
        }
        self.crawl(url, data=data, callback=self.index_page)

    @config(age=60 * 60)
    def index_page(self, response):
        json_response = json.loads(response.text)
        print(json_response)
        _sum = json_response.get("total")
        print(_sum)
        result = _sum // 10 + 1 if (_sum % 10) > 0 else _sum // 10
        # 爬虫只爬网站的前500页
        for n in range(1, 501):
            url = 'http://www.zjsfgkw.cn/Notice/NoticeSDSearch#{}'.format(n)
            data = {
                'pageno': str(n),
                'pagesize': '10'
            }
            self.crawl(url, data=data, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        # 初始化字段
        _id = ''
        ann_type = '送达公告'
        announcer = ''
        defendant = ''
        defendant_origin = ''
        ann_date = ''
        ann_content = ''
        ann_html = ''
        content_url = response.url
        pdf_url = ''
        case_no = ''
        source = '浙江法院公开网'
        try:
            json_response = json.loads(response.text)
            # print(json_response)
            result = json_response.get('list')
            for _list in result:
                ann_content = _list.get('Content')
                # print(ann_content)
                announcer = _list.get('Court')
                if not announcer:
                    announcer = ''
                case_no = _list.get('CaseNo')
                # print(2,3,re.findall(r'(^.*?)[：:]', ann_content)[0])
                a = re.findall(r'(^.*?)[：:]', ann_content)
                if len(a) == 0:
                    defendant = ''
                else:
                    defendant = re.findall(r'(^.*?)[：:]', ann_content)[0].replace('、', ',')
                print(defendant)
                url = "http://www.zjsfgkw.cn/Notice/NoticeSDInfo/" + str(_list.get('Notice_SD_ID'))
                long_time = _list.get('Time')
                print(long_time)
                timeStamp = re.findall(r'Date\((.*)\)/', str(long_time))[0]
                print(timeStamp)
                long = int(timeStamp) // 1000
                timeArray = time.localtime(long)
                ann_date = time.strftime("%Y-%m-%dT00:00:00+08:00", timeArray)

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
