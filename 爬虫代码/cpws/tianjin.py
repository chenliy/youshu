#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/11 14:00
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

from pyspider.libs.base_handler import *
import re
from urllib.parse import unquote
import requests
from pyquery import PyQuery as pq
import datetime
from IKEA.cpws.run_zy import process_ws #http://10.1.5.160:5000 上有


class Handler(BaseHandler):
    crawl_config = {
        'itag': 'beijing_day_6.23',
        'proxy': 'H21WNK49K6PFSR3P:BF2B9DDE973F0C02@http-pro.abuyun.com:9010',
    }

    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'tjhsfy.chinacourt.org',
            'If-Modified-Since': 'Mon, 09 Jul 2018 01:19:09 GMT',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
        }

    @every(minutes=24 * 60)
    def on_start(self):
        # 民事文书
        for i in range(1, 19):
            url = 'http://tjhsfy.chinacourt.org/paper/more/paper_mid/MzA0gAMA/page/{}.shtml'.format(i)
            html = requests.get(url, headers=self.headers).text
            p = pq(html)
            fabu_time = p('#list > ul > li:nth-child(1) > span.right').text()
            print(fabu_time)
            fabu_time = datetime.datetime.strptime(fabu_time, '%Y-%m-%d')
            self.crawl(url, headers=self.headers, save={'case_type': '民事文书', 'time': fabu_time},
                       callback=self.index_page)

        # 行政文书
        for j in range(1, 2):
            url = 'http://tjhsfy.chinacourt.org/paper/more/paper_mid/MzA2gAMA/page/{}.shtml'.format(j)
            print(url)
            html = requests.get(url, headers=self.headers).text
            p = pq(html)
            fabu_time = p('#list > ul > li:nth-child(1) > span.right').text()
            print(fabu_time)
            fabu_time = datetime.datetime.strptime(fabu_time, '%Y-%m-%d')
            self.crawl(url, headers=self.headers, save={'case_type': '行政文书', 'time': fabu_time},
                       callback=self.index_page)

        # 执行文书
        for k in range(1, 8):
            url = 'http://tjhsfy.chinacourt.org/paper/more/paper_mid/MzAxgAMA/page/{}.shtml'.format(k)
            print(url)
            html = requests.get(url, headers=self.headers).text
            print(3)
            p = pq(html)
            fabu_time = p('#list > ul > li:nth-child(1) > span.right').text()
            print(fabu_time)
            fabu_time = datetime.datetime.strptime(fabu_time, '%Y-%m-%d')
            self.crawl(url, headers=self.headers, save={'case_type': '执行文书', 'time': fabu_time},
                       callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        case_type = response.save['case_type']
        cookies = response.cookies
        time = response.save['time']
        print(time)
        for each in response.doc('div#list.font14 > ul > li  >span >a').items():
            url = each.attr['href']
            print(url)
            title = each.attr['title']
            print(title)
            self.crawl(url, headers=self.headers, save={'case_type': case_type, 'time': time,
                                                        'title': title}, cookies=cookies, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        case_type = response.save['case_type']
        time = response.save['time']
        title = response.save['title']
        html = response.text
        articles_doc = response.text
        patten = re.findall(r'tm\[.*?\]\=\"(.*?)\"', html)
        result = ''
        for x in patten:
            text = self.reverse_urlDecode_string(x)
            result = result + text

        print(result)
        try:
            time_xq = re.compile(r'(二[一二三四五六七八九十年月日Ο０ＯО0Oo○〇?]+)', re.S).findall(result)[-1].replace('?',
                                                                                                     'O')  # 如果有问号的话用大写的o代替
        except:
            time_xq = ''
        try:
            content_type = re.compile('<li class="type">(.*?)</li>', re.S).findall(result)[0]
        except:
            content_type = ''
        try:
            court_name = re.compile('<li class="title"><b>(.*?)</b></li>', re.S).findall(result)[0]
        except:
            court_name = ''
        try:
            case_no = re.compile('<li class="number">(.*?)</li>', re.S).findall(result)[0]
        except:
            case_no = ''
        try:
            publish_date = re.compile(r'<span>([\d:-].*?)</span>', re.S).findall(result)[0]
        except:
            publish_date = ''

        source = '天津海事法院'
        r1 = u'[a-zA-Z<>=]+'
        articles = re.sub(r1, '', result)

        yield {
            'title': title,
            'publish_date': time,
            'case_no': case_no,
            'articles': str(articles),
            'html': str(articles_doc),
            'type': case_type,  # 字段是那个字段，还要把..文书，改成什么什么案件
            'court_name': court_name,
            'content_type': content_type,
            'source': source,
            'org_url': response.url,
            'trial_date': '',
            'trial_round': '',
            'reason': '',
        }

    def reverse_urlDecode_string(self, string_text):
        encoding_text = unquote(string_text)
        html_text = encoding_text.replace('%', '\\').replace(';psbn&', '').encode('utf-8', 'ignore').decode(
            'unicode-escape', 'ignore')
        return html_text[::-1]

    def on_result(self, result):
        if not result:
            return
        print(result)
        process_ws(result)