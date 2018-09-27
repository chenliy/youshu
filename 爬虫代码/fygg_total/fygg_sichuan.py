#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/30 16:53
# Project:
# @Author: ZQJ
# @Email : zihe@yscredit.com

from pyspider.libs.base_handler import *
from lxml import etree
import re
import json
from lxml import html


class Handler(BaseHandler):
    crawl_config = {
        'itag': 'v6.11',
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

    data = {
        'ah': '',
        'page': '1',
        'fydm': '51',
        'limit': '9',
        'nd': '',
    }

    @every(minutes=24 * 60)
    @config(age=60 * 60)
    def on_start(self):

        url = 'http://111.230.134.78/sdgl/app/sdggsd_list'
        self.crawl(url, callback=self.get_page, method='POST', data=self.data)

    @config(age=60 * 60)
    def get_page(self, response):
        data = json.loads(response.content.decode('utf-8', errors='ignore'))
        all_page = data['totalPage']
        # print(all_page)
        for i in range(1, int(all_page) + 1):
            self.data['page'] = str(i)
            self.crawl(response.url + '#{}'.format(str(i)), callback=self.index_page, method='POST', data=self.data)

    @config(age=60 * 60)
    def index_page(self, response):
        js = json.loads(response.text)
        data = js['data']
        for each in data:
            ggsdid = each['ggsdid']
            ggbt = html.fromstring(each['ggbt']).text
            ssfy = html.fromstring(each['ssfy']).text  # 法院
            mc = html.fromstring(each['mc']).text  # 当事人
            clsj = html.fromstring(each['clsj']).text  # 时间
            ah = html.fromstring(each['ah']).text
            fydm = html.fromstring(each['fydm']).text
            # print(ggbt,'\n',ssfy,'\n',mc,'\n',clsj,'\n',ah,'\n',fydm)
            save = {
                'case_on': ah,
                'announcer': ssfy,
                'defendant': mc,
                'ann_date': clsj,
                'ggsdid': ggsdid
            }

            url = 'http://111.230.134.78/sdgl/app/getGgsdInfo.do'
            data = {
                'ggsdid': ggsdid,
                'ssfy': fydm
            }
            self.crawl(url + '#{}'.format(str(ggsdid)), callback=self.detail_page, method='POST', data=data, save=save)

    @config(priority=2)
    def detail_page(self, response):
        js = json.loads(response.text)
        print(js)
        data = js['data']['GGNR']
        ann_content = html.fromstring(data).text
        announcer = response.save['announcer']
        defendant = response.save['defendant']
        case_on = response.save['case_on']
        date = response.save['ann_date'].split(' ')
        content_url = response.url + '&' + response.save['ggsdid']
        ann_date = date[0] + 'T' + date[1] + ':00+08:00'

        yield {
            'ann_type': '送达公告',
            'announcer': str(announcer),
            'defendant': str(defendant),
            'case_no': str(case_on),
            'ann_content': str(ann_content),
            'ann_date': str(ann_date),
            'content_url': str(content_url),
            'ann_html': str(js),
            'pdf_url': '',
            'source': '四川法院司法公开网',
            'id': '',
            '_id_': ''

        }