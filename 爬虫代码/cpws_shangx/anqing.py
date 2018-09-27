#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/20 11:40
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

from pyspider.libs.base_handler import *
import re
from urllib.parse import unquote
from pyquery import PyQuery as pq
from IKEA.cpws.run_zy import process_ws


class Handler(BaseHandler):
    crawl_config = {
        'itag': 'beijing_day_6.23',
        'proxy': 'H21WNK49K6PFSR3P:BF2B9DDE973F0C02@http-pro.abuyun.com:9010',
    }

    retry_delay = {
        0: 60,
        1: 60 * 5,
        2: 60 * 10,
        3: 60 * 15,
        4: 60 * 20,
        5: 60 * 25,
    }

    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.sxcourt.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
        }

    @every(minutes=24 * 60)
    def on_start(self):

        for i in range(1, 10):
            url = 'http://www.aqzy.gov.cn/content/channel/529fdcbb259534f80e000001/page-{}/'.format(i)
            self.crawl(url, headers=self.headers, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):

        cookies = response.cookies

        time = []
        titles = []
        url = []

        for each in response.doc('ul.is-listnews li a[href]').items():
            titles.append(each.text())
            url.append(each.attr['href'])
        for each in response.doc('ul.is-listnews li span').items():
            time.append(each.text())

        if len(time) == len(url) == len(titles):
            for i in range(len(time)):
                self.crawl(url[i], headers=self.headers,
                           save={'title': titles[i], 'time': time[i]},cookies = cookies,
                           callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):

        time = response.save['time']
        # 要将时间转为日期格式
        a = re.compile('\d{2,4}', re.S).findall(time)
        time = '-'.join(a)

        result = response.text
        title = response.save['title']

        source = '安庆法院网'
        p = pq(result)
        total = []
        articles_doc = result
        print(articles_doc)
        try:
            title = re.compile('ass="is-newstitle">(.*?)</di').findall(result)[0]
        except:
            print(1)
        print(title)
        for each in p('div.is-newscontnet> div:nth-child(1) > *').items():
            if each.text:
                a = each.text().replace(' ', '').replace('\u3000', '').replace('\xa0', '').strip().split('\n')
                total = total + a
        b = []
        for x in total:
            if x != '':
                b.append(x)

        articles = str(b)
        if "发布日期" or '提交日期' not in b[1]:
            try:
                case_no = b[2]
            except:
                case_no = ''
            try:
                case_type = b[1][:2] + '案件'
                content_type = b[1][-3:]
            except:
                case_type = ''
                content_type = ''
            try:
                court_name = b[0]
            except:
                court_name = ''
        else:
            try:
                case_no = b[4]
            except:
                case_no = ''
            try:
                case_type = b[3][:2] + '案件'
                content_type = b[3][-3:]
            except:
                case_type = ''
                content_type = ''
            try:
                court_name = b[2]
            except:
                court_name = ''
        try:
            time_xq = re.compile(r'(二[一二三四五六七八九十年月日 Ο０〇ＯО0Oo○?]+)', re.S).findall(result)[-1].replace('?',
                                                                                                      'O')  # 如果有问号的话用大写的o代替
        except:
            time_xq = ''

        yield {
            'title': title,
            'publish_date': time,
            'case_no': case_no,
            'articles': str(articles),
            'html': str(articles_doc),
            'type': case_type,
            'court_name': court_name,
            'content_type': content_type,
            'source': source,
            'org_url': response.url,
            'trial_date': '',
            'trial_round': '',
            'reason': '',
        }

    def on_result(self, result):
        if not result:
            return
        print(result)
        process_ws(result)

