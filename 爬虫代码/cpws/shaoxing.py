#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/12 17:23
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
            'Host': 'www.sxcourt.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
        }

    @every(minutes=24 * 60)
    def on_start(self):

        # 知识产权裁判
        for i in range(1, 198):
            url = 'http://www.sxcourt.gov.cn/E_type.asp?E_typeid=27&page={}'.format(i)
            self.crawl(url, headers=self.headers, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        print(response.url)
        html = response.text
        time = []
        titles = []
        url = []
        for each in response.doc('div.area_son div.box.clearfix  ul.list_title div.list_box  a.title').items():
            titles.append(each.text())
            url.append(each.attr['href'])
        for each in response.doc('div.area_son div.box.clearfix  ul.list_title div.list_box  span.datetime').items():
            time.append(each.text())
        print(len(titles))
        print(titles)
        print(url)
        print(len(url))
        print(len(time), len(url), len(titles))

        if len(time) == len(url) == len(titles):
            for i in range(len(time)):
                self.crawl(url[i], headers=self.headers,
                           save={'title': titles[i], 'time': time[i]},
                           callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        time = response.save['time']
        print(time)
        result = response.text
        title = response.save['title']
        print(title)
        source = '绍兴市中级人民法院'
        p = pq(result)
        total = []
        articles_doc = p('div')
        for each in p('div.content > *').items():
            if each.text:
                a = each.text().replace(' ', '').replace('\u3000', '').replace('\xa0', '').strip().split('\n')
                total = total + a
        b = []
        for x in total:
            if x != '':
                b.append(x)
        print(b)
        for i in range(len(b) - 7):
            print(b[i])
            if len(b[i]) == 1:
                j = i + 1
                while len(b[j]) == 1:
                    b[i] = b[i] + b[j]
                    b.pop(j)
        print(b)
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

