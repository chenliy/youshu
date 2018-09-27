#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/27 10:42
# Project:
# @Author: ZQJ
# @Email : zihe@yscredit.com

from pyspider.libs.base_handler import *
import re
import json
import random
import time


class Handler(BaseHandler):
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

    crawl_config = {
        'itag': '7.26',
        # 'time_out': 8000,
        'proxy': 'H21WNK49K6PFSR3P:BF2B9DDE973F0C02@http-pro.abuyun.com:9010'
    }
    retry_delay = {
        0: 60,
        1: 60 * 1,
        2: 60 * 2,
        3: 60 * 3,
        4: 60 * 4,
        5: 60 * 5,
    }

    def __init__(self):
        self.UA = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        ]
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '30',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'www.zjsfgkw.cn',
            'Origin': 'http://www.zjsfgkw.cn',
            'Referer': 'http://www.zjsfgkw.cn/Notice/NoticeSDList',
            'User-Agent': random.choice(self.UA),
            'X-Requested-With': 'XMLHttpRequest'
        }

    @every(minutes=24 * 60)
    def on_start(self):
        headers = {
            'Host': 'www.zjsfgkw.cn',
            'Origin': 'http://www.zjsfgkw.cn',
            'User-Agent': random.choice(self.UA),
        }
        url = 'http://www.zjsfgkw.cn/Notice/NoticeSDList'
        self.crawl(url, headers=headers, callback=self.get_cbfy)

    @config(priority=2)
    def get_cbfy(self, response):

        cookies = response.cookies

        city_code = {}
        for each in response.doc('div.selectCourtUL  ul > li').items():
            city_code[each.text()] = each.attr['fyid']

        code_list = ['']

        for value in city_code.values():
            code_list.append(value)

        for cbfy in code_list:
            url = 'http://www.zjsfgkw.cn/Notice/NoticeSD#{}'.format(cbfy)
            data = {
                'pageno': '1',
                'pagesize': '10',
                'cbfy': cbfy
            }
            self.crawl(url, save={'cbfy': cbfy}, headers=self.headers, method='POST', data=data, cookies=cookies,
                       callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        cookies = response.cookies
        cbfy = response.save['cbfy']
        #print(cbfy)
        response_json = json.loads(response.text)
        #print(response_json)
        total_num = response_json.get('total', 1)
        #print(total_num)
        result = total_num // 10 + 1 if (total_num % 10) > 0 else total_num // 10
        for i in range(1, result + 1):
            url = 'http://www.zjsfgkw.cn/Notice/NoticeSD#{}{}'.format(cbfy, i)
            data = {
                'pageno': str(i),
                'pagesize': '10',
                'cbfy': cbfy
            }
            self.crawl(url, save={'cbfy': cbfy}, headers=self.headers, cookies=cookies, method='POST', data=data,
                       callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        # 初始化字段
        ann_type = '送达公告'
        ann_html = ''
        pdf_url = ''
        source = '浙江法院公开网'

        try:
            json_response = json.loads(response.text)
            # print(json_response)
            # print(json_response)
            result = json_response.get('list', '')
            for _list in result:
                ann_content = _list.get('Content', '')
                # print(ann_content)
                announcer = _list.get('Court', '')
                case_no = _list.get('CaseNo', '')

                # print(2,3,re.findall(r'(^.*?)[：:]', ann_content)[0])
                a = re.findall(r'(^.*?)[：:]', ann_content)
                if len(a) == 0:
                    defendant = ''
                else:
                    defendant = re.findall(r'(^.*?)[：:]', ann_content)[0].replace('、', ',')

                # print(defendant)
                url = "http://www.zjsfgkw.cn/Notice/NoticeSDInfo/" + str(_list.get('Notice_SD_ID', ''))
                # print(url)
                long_time = _list.get('Time', '')
                # print(long_time)
                timeStamp = re.findall(r'Date\((.*)\)/', str(long_time))[0]
                # print(timeStamp)
                long = int(timeStamp) // 1000
                timeArray = time.localtime(long)
                ann_date = time.strftime("%Y-%m-%dT00:00:00+08:00", timeArray)

                yield {
                    "ann_type": ann_type,
                    "announcer": announcer,
                    "case_no": case_no,
                    "ann_content": ann_content,
                    "ann_date": ann_date,
                    "content_url": url,
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

