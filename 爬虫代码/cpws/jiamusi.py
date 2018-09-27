#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/12 15:14
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

from pyspider.libs.base_handler import *
import re
from urllib.parse import unquote
from pyquery import PyQuery as pq


class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'yunsuo_session_verify=07bc00e22f8254d3bd588c83cff42dee',
            'Host': 'jmszy.hljcourt.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
        }

    @every(minutes=24 * 60)
    def on_start(self):
        # 民事文书
        for i in range(1, 25):
            url = 'http://jmszy.hljcourt.gov.cn/public/index.php?p={}&module=Paper&controller=Index&action=Index&LocationID=0900000000&enable=1&audit=1&foreign=0&excellent=0&cat1_id=&cat2_id=&cat3_id=&court_id=195&user_court_id=195'.format(
                i)
            self.crawl(url, headers=self.headers, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        a = response.doc('td.td_line a[href]').items()
        b = response.doc('td.td_time').items()
        time = []
        for each in b:
            print(each.text())
            time.append(each.text())
        titles = []
        url = []
        for each in a:
            href = each.attr['href']
            if len(href) < 100 and 'id' in href:
                url.append(href)
                title = each.text()
                print(title)
                print(href)
                titles.append(title)
        if len(time) == len(url) == len(titles):
            for i in range(len(time)):
                self.crawl(url[i], headers=self.headers, save={'title': titles[i], 'time': time[i]},
                           callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        time = response.save['time']
        print(time)
        result = response.text
        title = response.save['title']
        source = '佳木斯中级人民法院'
        p = pq(result)
        total = []
        articles_doc = p('div')
        for each in p('div#cc > *').items():
            if each.text:
                a = each.text().replace(' ', '').replace('\u3000', '').replace('\xa0', '').strip().split('\n')
                total = total + a
        b = []
        for x in total:
            if x != '':
                b.append(x)
        print(type(b))
        print(b[0])
        articles = str(b)
        if "提交日期" not in b[1]:
            try:
                case_no = b[2]
            except:
                case_no = ''
            try:
                content_type = b[1][:2] + '案件'
                case_type = b[1][-3:]
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
                content_type = b[3][:2] + '案件'
                case_type = b[3][-3:]
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
        print(time_xq)
        print(court_name)
        print(case_type)
        print(case_no)
        print(content_type)
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
            'trial_date': time_xq,
            'trial_round': '',
            'reason': '',
        }

