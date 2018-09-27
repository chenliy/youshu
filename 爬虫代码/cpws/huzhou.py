#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/12 16:30
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
            'Cookie': 'acw_tc=AQAAAGMsizsMTAoAPCGdt+qt/jBSVxkf; SERVERID=e146d554a29ee4143047c903abfbc3da|1531380212|1531379774',
            'Host': 'huzhou.zjcourt.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
        }

    @every(minutes=24 * 60)
    def on_start(self):

        # 知识产权裁判
        for i in range(1, 7):
            url = 'http://huzhou.zjcourt.cn/col/col1227191/index.html?uid=4391827&pageNum={}'.format(i)
            self.crawl(url, headers=self.headers, callback=self.index_page)
        # 刑事裁判
        for i in range(1, 15):
            url = 'http://huzhou.zjcourt.cn/col/col1227189/index.html?uid=4391827&pageNum={}'.format(i)
            self.crawl(url, headers=self.headers, callback=self.index_page)
            # 民事裁判
        for i in range(1, 101):
            url = 'http://huzhou.zjcourt.cn/col/col1227190/index.html?uid=4391827&pageNum={}'.format(i)
            self.crawl(url, headers=self.headers, callback=self.index_page)

        # 行政裁判
        for i in range(1, 7):
            url = 'http://huzhou.zjcourt.cn/col/col1227192/index.html?uid=4391827&pageNum={}'.format(i)
            self.crawl(url, headers=self.headers, callback=self.index_page)

        # 执行裁判
        url = 'http://huzhou.zjcourt.cn/col/col1227193/index.html'
        self.crawl(url, headers=self.headers, callback=self.index_page)
        # 再审裁判
        for i in range(1, 57):
            url = 'http://huzhou.zjcourt.cn/col/col1227194/index.html?uid=4391827&pageNum={}'.format(i)
            self.crawl(url, headers=self.headers, callback=self.index_page)
        # 减刑、假邢裁判
        for i in range(1, 4):
            url = 'http://huzhou.zjcourt.cn/col/col1227195/index.html?uid=4391827&pageNum={}'.format(i)
            self.crawl(url, headers=self.headers, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        print(response.url)
        html = response.text
        url = re.compile('font-size:14px;\'  href=\'(.*?html)', re.S).findall(html)
        time = re.compile('font-size:10.5pt>(.*?)</font', re.S).findall(html)
        titles = re.compile('title=\'(.*?)\'>', re.S).findall(html)
        print(time)
        print(url)
        print(titles)
        print(len(time), len(url), len(titles))

        if len(time) == len(url) == len(titles):
            for i in range(len(time)):
                self.crawl('http://huzhou.zjcourt.cn' + url[i], headers=self.headers,
                           save={'title': titles[i], 'time': time[i]},
                           callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        time = response.save['time']
        print(time)
        result = response.text
        title = response.save['title']
        print(title)
        source = '湖州市中级人民法院'
        p = pq(result)
        total = []
        articles_doc = p('div')
        for each in p('div#contents > *').items():
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
        if "发布日期" not in b[1]:
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

