# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/27 10:42
# Project: 法院公告-广东-广州
# @Author: ZQJ
# @Email : zihe@yscredit.com

from pyspider.libs.base_handler import *
from lxml import etree
import re
import logging
from datetime import datetime
import hashlib
import json
import requests

# 日志输出等级
logging.basicConfig(level=logging.info)


class Handler(BaseHandler):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Host': 'www.gd.xinhuanet.com'
    }

    crawl_config = {
        'itag': 'v1.0.2',
        'headers': headers,
        'time_out': 4000,
        # 'proxy': 'H14LXDJ6O07CAFDP:150D24D434AC09EE@proxy.abuyun.com:9010'
    }

    retry_delay = {
        0: 60,
        1: 60 * 5,
        2: 60 * 10,
        3: 60 * 15,
        4: 60 * 20,
        5: 60 * 25,
        6: 60 * 30,
        7: 60 * 35,
        8: 60 * 40,
        9: 60 * 45,
        10: 60 * 50,
        11: 60 * 55,
        12: 60 * 60,
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

    def escape(self, string):
        return '%s' % string

    def parse_time(self, t):
        t = list(t)
        d = {
            '零': '0',
            '一': '1',
            '二': '2',
            '三': '3',
            '四': '4',
            '五': '5',
            '六': '6',
            '七': '7',
            '八': '8',
            '九': '9',
            '○': '0',
            'Ｏ': '0',
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

    def ines(self, host, id, path, data):
        # host = 'http://10.20.20.106:9200/'
        for d in data:
            if data[d] == '' or data[d] == 'null':
                data[d] = None
        data = json.dumps(data)
        url = '{}/{}'.format(host + path, id)
        print(url)
        html = requests.post(url, data=data)
        return url

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

    @every(minutes=24 * 60)
    def on_start(self):
        url = 'http://www.gd.xinhuanet.com/zt16/gzzy/index.htm#start'
        self.crawl(url, callback=self.get_pages)
        url = 'http://www.gd.xinhuanet.com/zt16/gzzy/index.htm'
        self.crawl(url, callback=self.get_lists)

    @config(age=12 * 60 * 60)
    def get_pages(self, response):
        try:
            html = etree.HTML(response.text)
            logging.info('查找页数...')
            pages = html.xpath('//div[@id="div_currpage"]/a/text()')[-2]
            # logging.info(pages_url)
            # pages = re.findall(r'p=(\d*)',pages_url)[0]
            print(pages)
            if int(pages) >= 2:
                for page in range(2, int(pages) + 1):
                    url = 'http://www.gd.xinhuanet.com/zt16/gzzy/index_{}.htm'.format(str(page))
                    self.crawl(url, callback=self.get_lists, retries=12)
        except Exception as e:
            logging.info(e)
            logging.info('当前法院无内容...')

    @config(age=12 * 60 * 60)
    def get_lists(self, response):
        try:
            html = etree.HTML(response.text)
            results = html.xpath('//ul[@class="dataList"]//li')
            base_url = 'http://mdjzy.hljcourt.gov.cn'
            for result in results:
                list_response = etree.tounicode(result)
                url = result.xpath('.//a/@href')[0]
                title = result.xpath('.//a/text()')[0].strip()
                # url ='http://www.gd.xinhuanet.com/2017-12/13/c_1122105194.htm'
                # url ='http://www.gd.xinhuanet.com/2017-11/21/c_1121988802.htm'
                self.crawl(url, callback=self.get_detail, save={'list_response': list_response, 'title': title},
                           retries=12, allow_redirects=False)
        except Exception as e:
            logging.info(e)
            logging.info('当前法院无内容...')

    @config(age=12 * 60 * 60)
    @catch_status_code_error
    def get_detail(self, response):
        # 初始化字段
        ann_type = '送达公告'
        announcer = '广东省广州市中级人民法院'
        defendant = ''
        ann_date = ''
        ann_content = ''
        ann_html = ''
        content_url = response.url
        pdf_url = ''
        case_no = ''
        source = '广州市中级人民法院'

        list_response = response.save['list_response']
        title = response.save['title']
        # html = response.etree
        if response.status_code == 200:
            try:
                html = etree.HTML(response.text)
                detail = html.xpath('//div[@class="content"]')[0]
                ann_html = etree.tounicode(detail)
                # logging.info('开始结构化..')
                results = html.xpath('//div[@class="content"]/p//text()')
                results = [result.strip() for result in results if result.strip()]
                logging.info(results)
                ann_time = html.xpath('//div[@class="laiyuan"]/text()')[0].split('：')[-1]
                ann_date = self.parse_time(ann_time)
                for result in results:
                    if result.endswith('：') or result.endswith(':'):
                        if not ann_content:
                            ann_content = ''.join(results[results.index(result) + 1:])
                            defendant_origin = result.replace(':', '').replace('：', '')
                            if '、' in defendant_origin:
                                defendants = defendant_origin.split('、')
                            elif ',' in defendant_origin:
                                defendants = defendant_origin.split(',')
                            else:
                                defendants = [defendant_origin]
                            # ann_content = results[-3]
                            yield {
                                'ann_type': ann_type,
                                'announcer': announcer,
                                'defendant': str(defendants),
                                'ann_date': ann_date,
                                'ann_content': ann_content,
                                'ann_html': ann_html,
                                'content_url': content_url,
                                'pdf_url': pdf_url,
                                'source': source,
                                'case_no': case_no,
                                'id': '',
                                '_id_': ''
                            }
            except Exception as e:
                logging.warning('哪里可能出问题了...')
                logging.warning(e)






