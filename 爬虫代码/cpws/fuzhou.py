#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/12 20:04
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
            'Host': 'fzzy.chinacourt.org',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
        }

    def reverse_urlDecode_string(self, string_text):
        encoding_text = unquote(string_text)
        html_text = encoding_text.replace('%', '\\').replace(';psbn&', '').encode('utf-8', 'ignore').decode(
            'unicode-escape', 'ignore')
        return html_text[::-1]

    @every(minutes=24 * 60)
    def on_start(self):
        # 民事文书
        for i in range(1, 15):
            url = 'http://fzzy.chinacourt.org/paper/more/paper_mid/MzA0gAMA/page/{}.shtml'.format(i)
            # print(url)
            self.crawl(url, headers=self.headers, save={'case_type': '民事文书', 'special': 0}, callback=self.index_page)
        # 刑事文书
        for k in range(1, 5):
            url = 'http://fzzy.chinacourt.org/paper/more/paper_mid/MzAygAMA/page/{}.shtml'.format(i)
            self.crawl(url, headers=self.headers, save={'case_type': '刑事文书', 'special': 0}, callback=self.index_page)

        # 行政文书
        for j in range(1, 4):
            url = 'http://fzzy.chinacourt.org/paper/more/paper_mid/MzA2gAMA/page/{}.shtml'.format(i)
            self.crawl(url, headers=self.headers, save={'case_type': '行政文书', 'special': 0}, callback=self.index_page)

        # 执行文书
        url = 'http://fzzy.chinacourt.org/paper/more/paper_mid/MzAxgAMA.shtml'
        self.crawl(url, headers=self.headers, save={'case_type': '执行文书', 'special': 0}, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        a = response.doc('div#list ul li span a[href]').items()
        b = response.doc('span.right').items()
        time = []
        for each in b:
            print(each.text())
            time.append(each.text())
        titles = []
        url = []
        for each in a:
            href = each.attr['href']
            if len(href) < 100:
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
        html = response.text
        title = response.save['title']
        patten = re.findall(r'tm\[.*?\]\=\"(.*?)\"', html)
        result = ''
        for x in patten:
            text = self.reverse_urlDecode_string(x)
            result = result + text

        print(result)
        try:
            time_xq = \
                re.compile(r'(二[Ο○０ＯО0Oo〇?][Ο０ＯО○0Oo〇?一][一二三四五六七八九十年月日 Ο○０〇ＯО0Oo?]年[一二三四五六七八九十年月日 Ο○０〇ＯО0Oo?]+)',
                           re.S).findall(result)[-1].replace('?',
                                                             'O')  # 如果有问号的话用大写的o代替
        except:
            time_xq = ''
        print(time_xq)
        try:
            content_type = re.compile('class="type">(.*?)</li>', re.S).findall(result)[0].replace(' ', '').replace(
                '\u3000', '').replace('\xa0', '').replace(' ', '')
            if content_type != '':
                print(content_type)
                print(1)
                content_type = content_type[:2] + '案件'
                case_type = re.compile('class="type">(.*?)</li>', re.S).findall(result)[0].replace(' ', '').replace(
                    '\u3000', '').replace('\xa0', '')[-3:]
            if content_type == '':
                print(3)
                content_type = re.compile('</p><p>(.*?)<br />', re.S).findall(result)[0].replace(' ', '').replace(
                    '\u3000', '').replace('\xa0', '').replace(' ', '')[:2] + '案件'
                print(content_type, 4)
                case_type = re.compile('</p><p>(.*?)<br />', re.S).findall(result)[0].replace(' ', '').replace(
                    '\u3000', '').replace('\xa0', '')[-3:]

        except:
            print(2)
            content_type = ''
            case_type = ''
        print(content_type)
        try:
            court_name = re.compile('title"><b>(.*?)</b><', re.S).findall(result)[0]
        except:
            court_name = ''
        print(court_name)
        try:
            case_no = re.compile('ss="number">(.*?)</li>', re.S).findall(result)[0]
        except:
            case_no = ''
        print(case_no)
        try:
            publish_date = re.compile(r'0> ([\d-]+.*?)</FONT></DIV>', re.S).findall(result)[0]
        except:
            publish_date = ''
        print(publish_date)
        source = '抚州法院网'
        p = pq(result)
        total = []
        articles_doc = p('div')
        for each in p('div > *').items():
            if each.text:
                a = each.text().replace(' ', '').replace('\u3000', '').replace('\xa0', '').strip().split('\n')
                total = total + a
        b = []
        for x in total:
            if x != '':
                b.append(x)
        print(b)
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
            'trial_date': time_xq,
            'trial_round': '',
            'reason': '',
        }
