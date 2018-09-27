#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/10 10:10
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

from pyspider.libs.base_handler import *
import re
from urllib.parse import unquote


# 北京裁判文书2014年前数据全量


class Handler(BaseHandler):
    crawl_config = {
        'itag': 'beijing_day_6.23',
        'proxy': 'H21WNK49K6PFSR3P:BF2B9DDE973F0C02@http-pro.abuyun.com:9010',
    }

    # 民事文书 http://bjgy.chinacourt.org/paper/more/paper_mid/MzA0gAMA/page/1.shtml 314页
    # 刑事文书 http://bjgy.chinacourt.org/paper/more/paper_mid/MzAygAMA.shtml 1页
    # 行政文书 http://bjgy.chinacourt.org/paper/more/paper_mid/MzA2gAMA/page/1.shtml 10页
    # 没有执行文书，由于只爬全量不更新就不写了
    # 涉外文书脑残，首页有，点击more却为空

    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': ' bjgy.chinacourt.org',
            'If-Modified-Since': 'Mon, 09 Jul 2018 01:19:09 GMT',
            'If-None-Match': ' W/"5b42b80d-7db4"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
        }
        self.headers2 = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'h-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': ' keep-alive',

            'Host': 'bjgy.chinacourt.org',
            'If-Modified-Since': 'Wed, 22 Nov 2017 02:54:13 GMT',
            'If-None-Match': 'W/"5a14e6d5-7091"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
        }

    @every(minutes=24 * 60)
    def on_start(self):
        # 民事文书
        for i in range(1, 315):
            url = 'http://bjgy.chinacourt.org/paper/more/paper_mid/MzA0gAMA/page/{}.shtml'.format(i)
            # print(url)
            self.crawl(url, headers=self.headers2, save={'case_type': '民事文书',
                                                         'special': 0}, callback=self.index_page)
        # 刑事文书
        url = 'http://bjgy.chinacourt.org/paper/more/paper_mid/MzAygAMA.shtml'
        self.crawl(url, headers=self.headers2, save={'case_type': '刑事文书',
                                                     'special': 0}, callback=self.index_page)

        # 行政文书
        for j in range(1, 11):
            url = 'http://bjgy.chinacourt.org/paper/more/paper_mid/MzA2gAMA/page/{}.shtml'.format(j)
            self.crawl(url, headers=self.headers2, save={'case_type': '行政文书',
                                                         'special': 0}, callback=self.index_page)
        # 执行文书
        # 涉外文书
        url = 'http://bjgy.chinacourt.org/paper.shtml'
        self.crawl(url, headers=self.headers2, save={'case_type': '涉外文书',
                                                     'special': 1}, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        case_type = response.save['case_type']
        print(case_type)
        special = response.save['special']
        cookies = response.cookies
        if special == 0:
            for each in response.doc('div#list.font14 > ul > li  >span >a').items():
                url = each.attr['href']
                print(url)
                title = each.attr['title']
                print(title)
                self.crawl(url, headers=self.headers2, save={'case_type': case_type,
                                                             'title': title,
                                                             'special': 0}, cookies=cookies, callback=self.detail_page)
        if special == 1:
            for each in response.doc('#main > div.content > .yui3-g.list_br li a').itenm():
                url = each.attr['href']
                print(url)
                title = each.attr['title']
                print(title)
                self.crawl(url, headers=self.headers2, save={'case_type': case_type,
                                                             'title': title,
                                                             'special': 0}, cookies=cookies, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        case_type = response.save['case_type']
        title = response.save['title']
        html = response.text

        patten = re.findall(r'tm\[.*?\]\=\"(.*?)\"', html)
        result = ''
        for x in patten:
            text = self.reverse_urlDecode_string(x)
            result = result + text

        print(result)
        try:
            time = re.compile(r'(二[一二三四五六七八九十年月日月 0Oo○〇?]+)', re.S).findall(result)[-1].replace('?',
                                                                                                'O')  # 如果有问号的话用大写的o代替
        except:
            time = ''
        print(time)
        try:
            content_type = re.compile('<li class="type">(.*?)</li>', re.S).findall(result)[0]
        except:
            content_type = ''
        # print(case_type)
        try:
            court_name = re.compile('<li class="title"><b>(.*?)</b></li>', re.S).findall(result)[0]
        except:
            court_name = ''
        # print(court_name)
        try:
            case_no = re.compile('<li class="number">(.*?)</li>', re.S).findall(result)[0]
        except:
            case_no = ''
        # print(case_no)
        try:
            publish_date = re.compile(r'<span>([\d:-].*?)</span>', re.S).findall(result)[0]
        except:
            publish_date = ''
        # print(publish_date)
        source = '北京法院网'
        r1 = u'[a-zA-Z<>=]+'
        articles = re.sub(r1, '', result)
        # print(articles)
        # print(result,case_type,court_name,case_no,publish_date,articles)
        yield {
            'title': title,
            'case_no': case_no,
            'publish_date': publish_date,
            'articles': articles,
            'type': case_type,
            'court_name': court_name,
            'source': source,
            'org_url': response.url,
            'trial_date': time
        }

    def reverse_urlDecode_string(self, string_text):
        encoding_text = unquote(string_text)
        html_text = encoding_text.replace('%', '\\').replace(';psbn&', '').encode('utf-8', 'ignore').decode(
            'unicode-escape', 'ignore')
        return html_text[::-1]

