#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-07-05 09:45:24
# Project: sc_fygg
# @Author: ZQJ
# @Email : zihe@yscredit.com
from pyspider.libs.base_handler import *
import json
from lxml import html


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
                  {"name": "defendant", "type": "string"}
                  ]

    def __init__(self):

        self.url0 = 'http://zxgk.sccourt.gov.cn/webapp/area/scsfgk/sfgk/ggsd/ggsd-main.jsp'

        # 直接按查询得到post请求
        # 这个post请求时常会变要注意
        self.url1 = 'http://111.230.134.78:8081/sdgl/app/sdggsd_list'

        self.data = {
            'ah': '',
            'page': '1',
            'fydm': '51',
            'limit': '9',
            'nd': '',
        }
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'h-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '30',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': '111.230.134.78:8081',
            'Origin': 'http://111.230.134.78:8081',
            'Referer': 'http://111.230.134.78:8081/sdgl/webapp/sfsdweb/notice_no.html?fydm=51',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

    crawl_config = {
        'itag': 'v6.11',
        'time_out': 4000,
        'proxy': 'H21WNK49K6PFSR3P:BF2B9DDE973F0C02@http-pro.abuyun.com:9010'
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(self.url1, method='POST', headers=self.headers, data=self.data, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):

        print(response.text)
        json_data = json.loads(response.content.decode('utf-8', errors='ignore'))

        # 总页数
        all_page = json_data.get('totalPage', 0)
        print(all_page)

        # 通过控制self.data里面的page参数进行翻页
        for i in range(1, int(all_page) + 1):
            self.data['page'] = str(i)
            print(self.data)
            self.crawl(self.url1 + '#{}'.format(i), headers=self.headers, method='POST', data=self.data,
                       callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        content = json.loads(response.content.decode('utf-8', errors='ignore'))

        # 主要内容
        data = content.get('data', '')
        print(data)

        # html.fromstring 能起到解析的作用
        for each in data:
            ggsdid = each.get('ggsdid', '')
            ggbt = html.fromstring(each.get('ggbt', '')).text
            ssfy = html.fromstring(each.get('ssfy', '')).text  # 法院
            mc = html.fromstring(each.get('mc', '')).text  # 当事人
            clsj = html.fromstring(each.get('clsj', '')).text  # 时间
            ah = html.fromstring(each.get('ah', '')).text
            fydm = html.fromstring(each.get('fydm', '')).text
            # print(ggbt,'\n',ssfy,'\n',mc,'\n',clsj,'\n',ah,'\n',fydm)

            save = {
                'case_on': ah,
                'announcer': ssfy,
                'defendant': mc,
                'ann_date': clsj,
                'ggsdid': ggsdid
            }

            # 爬取详情页
            url = 'http://111.230.134.78:8081/sdgl/app/getGgsdInfo.do'  # 详情页链接，页面上点击之后最后一个post请求有
            data = {
                'ggsdid': ggsdid,
                'ssfy': fydm
            }
            #print(data)
            headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                       'Accept-Encoding': 'gzip, deflate',
                       'Accept-Language': 'zh-CN,zh;q=0.9',
                       'Connection': 'keep-alive',
                       'Content-Length': '51',
                       'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                       'Host': '111.230.134.78:8081',
                       'Origin': 'http://111.230.134.78:8081',
                       'Referer': 'http://111.230.134.78:8081/sdgl/webapp/sfsdweb/notice_detail_no.html?',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
                       '-Requested-With': 'XMLHttpRequest'
                       }
            self.crawl(url + '#{}'.format(str(ggsdid)), headers=headers, callback=self.findal_page, method='POST',
                       data=data, save=save)

    @config(priority=2)
    def findal_page(self, response):
        #print(response.url)
        content = json.loads(response.text)
        #print(content)
        data = content['data']
        if data == '':
            yield {
                'ann_type': '送达公告',
                'announcer': '',
                'defendant': '',
                'case_no': '',
                'ann_content': '',
                'ann_date': '',
                'content_url': '',
                'ann_html': '',
                'pdf_url': '',
                'source': '四川法院司法公开网',
                'id': '',
                '_id_': ''
            }
        else:
            data = data['GGNR']
            print(data)
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
                'ann_html': str(content),
                'pdf_url': '',
                'source': '四川法院司法公开网',
                'id': '',
                '_id_': ''

            }
