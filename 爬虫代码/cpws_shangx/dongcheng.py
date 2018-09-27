#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/20 11:47
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com


from pyspider.libs.base_handler import *
import re
from urllib.parse import unquote
from pyquery import PyQuery as pq
from IKEA.cpws.run_zy import process_ws


# 东城区裁判文书2015年前数据全量


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
            'Host': 'dcqfy.chinacourt.org',
            'If-Modified-Since': 'Mon, 09 Jul 2018 01:19:09 GMT',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
        }

    @every(minutes=24 * 60)
    def on_start(self):

        # 民事文书
        for i in range(1, 40):
            url = 'http://dcqfy.chinacourt.org/paper/more/paper_mid/MzA0gAMA/page/{}.shtml'.format(i)
            # print(url)
            self.crawl(url, headers=self.headers, save={'case_type': '民事案件',
                                                        'special': 0}, callback=self.index_page)
        # 刑事文书
        for j in range(1, 11):
            url = 'http://dcqfy.chinacourt.org/paper/more/paper_mid/MzAygAMA/page/{}.shtml'.format(j)
            self.crawl(url, headers=self.headers, save={'case_type': '刑事案件',
                                                        'special': 0}, callback=self.index_page)

        # 行政文书
        for k in range(1, 2):
            url = 'http://dcqfy.chinacourt.org/paper/more/paper_mid/MzA2gAMA.shtml'
            self.crawl(url, headers=self.headers, save={'case_type': '行政案件',
                                                        'special': 0}, callback=self.index_page)
        # 执行文书
        url = 'http://dcqfy.chinacourt.org/paper/more/paper_mid/MzAxgAMA.shtml'
        self.crawl(url, headers=self.headers, save={'case_type': '执行案件',
                                                    'special': 0}, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        case_type = response.save['case_type']

        b = response.doc('div#list.font14 ul li span.right').items()
        time = []
        for each in b:
            time.append(each.text())

        a = response.doc('div#list.font14 li a[href]').items()
        titles = []
        url = []
        for each in a:
            href = each.attr['href']
            if len(href) < 100:
                url.append(href)
                title = each.text()
                titles.append(title)

        if len(time) == len(url) == len(titles):
            for i in range(len(time)):
                self.crawl(url[i], headers=self.headers,
                           save={'title': titles[i], 'time': time[i], 'case_type': case_type},
                           callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):

        time = response.save['time']
        case_type = response.save['case_type']
        title = response.save['title']
        html = response.text

        patten = re.findall(r'tm\[.*?\]\=\"(.*?)\"', html)
        result = ''

        for x in patten:
            text = self.reverse_urlDecode_string(x)
            result = result + text

        articles_doc = result
        print(articles_doc)
        try:
            title = re.compile('class="title">(.*?)</li>', re.S).findall(result)[0]
        except:
            print(1)

        print(title)
        try:
            time_xq = re.compile(r'(二[一二三四五六七八九十年月日ΟО0Oo○〇?]+)', re.S).findall(result)[-1].replace('?',
                                                                                                   'O')  # 如果有问号的话用大写的o代替
        except:
            time_xq = ''

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
                    content_type = content_type[-2:] + '书'  # 有可能只有判决或者裁定两个字
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

        source = '北京市东城区人民法院'
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
