#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/20 10:57
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

from pyspider.libs.base_handler import *
import re
from urllib.parse import unquote
from pyquery import PyQuery as pq
from IKEA.cpws.run_zy import process_ws


# 北京裁判文书2014年前数据全量


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
            'Host': ' bjgy.chinacourt.org',
            'If-Modified-Since': 'Mon, 09 Jul 2018 01:19:09 GMT',
            'If-None-Match': ' W/"5b42b80d-7db4"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
        }

    @every(minutes=24 * 60)
    def on_start(self):

        # 民事文书
        for i in range(1, 315):
            url = 'http://bjgy.chinacourt.org/paper/more/paper_mid/MzA0gAMA/page/{}.shtml'.format(i)
            self.crawl(url, headers=self.headers, save={'case_type': '民事案件', 'special': 0}, callback=self.index_page)

        # 刑事文书
        url = 'http://bjgy.chinacourt.org/paper/more/paper_mid/MzAygAMA.shtml'
        self.crawl(url, headers=self.headers, save={'case_type': '刑事案件', 'special': 0}, callback=self.index_page)

        # 行政文书
        for j in range(1, 11):
            url = 'http://bjgy.chinacourt.org/paper/more/paper_mid/MzA2gAMA/page/{}.shtml'.format(j)
            self.crawl(url, headers=self.headers, save={'case_type': '行政案件', 'special': 0}, callback=self.index_page)

        # 涉外文书
        url = 'http://bjgy.chinacourt.org/paper.shtml'
        self.crawl(url, headers=self.headers, save={'case_type': '涉外案件', 'special': 1}, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):

        case_type = response.save['case_type']

        b = response.doc('div#list.font14 ul li span.right').items()
        time = []
        for each in b:
            time.append(each.text())

        special = response.save['special']

        cookies = response.cookies

        titles = []
        urls = []
        if special == 0:
            for each in response.doc('div#list.font14 > ul > li  >span >a').items():
                url = each.attr['href']
                urls.append(url)
                title = each.attr['title']
                titles.append(title)

            if len(urls) == len(titles) == len(time):
                for i in range(1, len(time) + 1):
                    self.crawl(urls[-i], headers=self.headers,
                               save={'case_type': case_type, 'title': titles[-i], 'time': time[-i], 'special': 0},
                               cookies=cookies, callback=self.detail_page)

        if special == 1:
            for each in response.doc('#main > div.content > .yui3-g.list_br li a').items():
                url = each.attr['href']
                urls.append(url)
                title = each.attr['title']
                titles.append(title)
            if len(urls) == len(titles) == len(time):
                for i in range(1, len(urls) + 1):
                    self.crawl(urls[-i], headers=self.headers,
                               save={'case_type': case_type, 'title': titles[-i], 'time': time[-i], 'special': 0},
                               cookies=cookies, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):

        title = response.save['title']
        time = response.save['time']
        case_type = response.save['case_type']

        html = response.text
        patten = re.findall(r'tm\[.*?\]\=\"(.*?)\"', html)
        result = ''
        for x in patten:
            text = self.reverse_urlDecode_string(x)
            result = result + text

        try:
            time_xq = re.compile(r'(二[一二三四五六七八九十年月日 Ο０ＯО0Oo○〇?]+)', re.S).findall(result)[-1].replace('?',
                                                                                                      'O')  # 如果有问号的话用大写的o代替
        except:
            time_xq = ''

        # content_type,先判断标题里有没有，没有的话再正则提取
        if '书' in title[-3:]:
            content_type = title[-3:]
        else:
            try:
                content_type = re.compile('<li class="type">(.*?)</li>', re.S).findall(result)[0].replace(' ',
                                                                                                          '').replace(
                    '\u3000', '').replace('\xa0', '')
                print(content_type)
                if '书' in content_type:
                    content_type = content_type[-3:]
                else:
                    content_type[-2:] + '书'  # 有可能只有判决或者裁定两个字
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

        source = '北京法院网'

        p = pq(result)
        total = []

        for each in p('div > *').items():
            if each.text:
                a = each.text().replace(' ', '').replace('\u3000', '').replace('\xa0', '').strip().split('\n')
                total = total + a
        b = []
        for x in total:
            if x != '':
                b.append(x)

        articles = str(b)
        title = b[0]
        print(b)
        articles_doc = p('div')
        yield {
            'title': title,
            'publish_date': time,
            'case_no': case_no,
            'articles': str(articles),
            'html': str(articles_doc),
            'type': case_type,  # 民事案件等
            'court_name': court_name,
            'content_type': content_type,  # 判决书等
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
        process_ws(result)