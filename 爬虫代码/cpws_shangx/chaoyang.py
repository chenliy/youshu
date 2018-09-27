#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/20 12:58
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
            'Host': 'cyqfy.chinacourt.org',
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
        for i in range(1, 233):
            url = 'http://cyqfy.chinacourt.org/public/cpws.php?p={}&module=Paper&controller=Index&action=Index&enable=1&audit=1&foreign=0&excellent=0&cat1_id=&cat2_id=&cat3_id=&reg_time=&casenumber=&title=&content='.format(
                i)
            self.crawl(url, headers=self.headers, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):

        cookie = response.cookies
        a = response.doc('td.br_list_1 a[href]').items()
        b = response.doc('td.td_time').items()
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
                           callback=self.detail_page, cookies=cookie)

    @config(priority=2)
    def detail_page(self, response):

        time = response.save['time']
        # 要将时间转为日期格式
        a = re.compile('\d{2,4}', re.S).findall(time)
        time = '-'.join(a)

        html = response.text

        title = response.save['title']

        patten = re.findall(r'tm\[.*?\]\=\"(.*?)\"', html)

        result = ''
        for x in patten:
            text = self.reverse_urlDecode_string(x)
            result = result + text
        articles_doc = result
        print(articles_doc)

        try:
            title = re.compile(' -->(.*?)</FONT', re.S).findall(result)[0]
        except:
            print(1)

        print(title)
        try:
            time_xq = re.compile(r'(二[一二三四五六七八九十年月日 ΟＯО0Oo○〇?]+)', re.S).findall(result)[-1].replace('?',
                                                                                                     'O')  # 如果有问号的话用大写的o代替
        except:
            time_xq = ''

        if '书' in title.replace(' ', '').replace('\u3000', '').replace('\xa0', '')[-3:]:
            content_type = title.replace(' ', '').replace('\u3000', '').replace('\xa0', '')[-3:]
            case_type = title.replace(' ', '').replace('\u3000', '').replace('\xa0', '')[-5:-3] + '案件'
        else:
            try:
                content_type = re.compile('<!--类型 -->(.*?)</td></tr>', re.S).findall(result)[0].replace(' ',
                                                                                                        '').replace(
                    '\u3000', '').replace('\xa0', '')[-3:]
                case_type = re.compile('<!--类型 -->(.*?)</td></tr>', re.S).findall(result)[0].replace(' ', '').replace(
                    '\u3000', '').replace('\xa0', '')[:2] + '案件'
            except:
                content_type = ''
                case_type = ''

        try:
            court_name = re.compile('SIZE="4">(.*?)</FONT>', re.S).findall(result)[0]
        except:
            court_name = ''

        try:
            case_no = re.compile('<!--案件号 -->(.*?)</td>', re.S).findall(result)[0]
        except:
            case_no = ''

        source = '北京市朝阳区法院网'
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

    def on_result(self, result):
        if not result:
            return
        print(result)
        process_ws(result)
