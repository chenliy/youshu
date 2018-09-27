#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/8/4 14:58
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

from pyspider.libs.base_handler import *
import re
from bs4 import BeautifulSoup


class Handler(BaseHandler):
    crawl_config = {
        'itag': 'v7.27',
        'time_out': 100000,

    }
    schema_def = [{"name": "id", "type": "string"},
                  {"name": "_id_", "type": "string"},
                  {"name": "ann_type", "type": "string"},
                  {"name": "announcer", "type": "string"},
                  {"name": "case_no", "type": "string"},
                  {"name": "ann_content", "type": "string"},
                  {"name": "ann_date", "type": "string"},
                  {"name": "content_url", "type": "string"},
                  {"name": "ann_html", "type": "string"},
                  {"name": "pdf_url", "type": "string"},
                  {"name": "source", "type": "string"},
                  {"name": "defendant", "type": "string"}
                  ]

    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'zip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Host': 'www.xmcourt.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
        }

    @every(minutes=24 * 60)
    def on_start(self):
        for i in range(1, 7):
            url = 'http://www.xmcourt.gov.cn/ygsf/jxssgs/index.htm?currpage={}'.format(i)
            self.crawl(url, callback=self.index_page, headers=self.headers)

    @config(age=60 * 60)
    def index_page(self, response):
        cookies = response.cookies
        urls = []
        titles = []
        for each in response.doc('div.xmfyw_srig li a[href]').items():
            print(each.attr['href'])
            urls.append(each.attr['href'])
            titles.append(each.text())
        times = []
        for each in response.doc('div.xmfyw_srig li span.tgrey2').items():
            times.append(each.text())
        print(len(times))
        print(len(urls))
        if len(urls) == len(times) == len(titles):
            for i in range(len(urls)):
                self.crawl(urls[i], callback=self.detail_page,
                           save={'title': titles[i], 'ann_date': times[i]},
                           cookies=cookies)

    @config(priority=2)
    def detail_page(self, response):

        title = response.save['title']
        print(title)
        if '开庭公告' in title:
            ann_type = '开庭公告'
            ann_date = response.save['ann_date']
            a = re.compile('\d{2,4}', re.S).findall(ann_date)
            ann_date = '-'.join(a) + 'T00:00:00+08:00'

            announcer = '厦门市中级人民法院'

            ann_content = title + '  ' + response.doc('div.xmfyw_sxl_con5.t14.h30').text().replace('\n', '').replace(
                ' ', '').replace('\u3000', '').replace('\xa0', '')

            ann_html = ann_content
            content_url = response.url
            defendant = ''
            case_no = ''
            pdf_url = ''
            yield {
                'id': '',
                '_id_': '',
                'ann_type': ann_type,
                'announcer': announcer,
                'defendant': defendant,
                'ann_date': ann_date,
                'ann_content': ann_content,
                'ann_html': ann_html,
                'content_url': content_url,
                'pdf_url': pdf_url,
                'case_no': case_no,
                'source': '厦门法院网',
            }


        else:
            ann_type = '送达公告'

            # print(ann_type)
            ann_date = response.save['ann_date']
            a = re.compile('\d{2,4}', re.S).findall(ann_date)
            ann_date = '-'.join(a) + 'T00:00:00+08:00'

            announcer = '厦门市中级人民法院'

            ann_content_first = response.doc('#fontzoom > div > p:nth-child(2) > span').text().replace('\n', '').replace(' ', '').replace( '\u3000', '').replace('\xa0', '')

            html = response.text
            soup = BeautifulSoup(html, 'lxml')

            trs = soup.find_all('tr')
            result_total = []

            for tr in trs:
                # print(tr.get_text().replace('\n\n','abc'))
                a = [x.replace('\n', '') for x in
                     re.compile(r'#?(.*?)#', re.S).findall(tr.get_text().replace('\n\n', '#'))]
                result_total.append(a)

            print(result_total)
            num = 0
            for i in range(len(result_total)-1):
                if len(result_total[i]) == len(result_total[i + 1]) == len(result_total[-1]):
                    title = result_total[i]
                    num = i
                    break

            if num != 0:
                for j in range(num + 1, len(result_total)):
                    result_dict = {}
                    if len(title) == len(result_total[j]):
                        for k in range(len(title)):
                            result_dict[title[k]] = result_total[j][k]

                    ann_content = ann_content_first + str(result_dict)
                    ann_html = ann_content
                    content_url = response.url
                    defendant = result_dict.get('姓名', '')
                    case_no = ''
                    # print(content_url)
                    # print(ann_html)
                    pdf_url = ''
                    yield {
                        'id': '',
                        '_id_': '',
                        'ann_type': ann_type,
                        'announcer': announcer,
                        'defendant': defendant,
                        'ann_date': ann_date,
                        'ann_content': ann_content,
                        'ann_html': ann_html,
                        'content_url': content_url,
                        'pdf_url': pdf_url,
                        'case_no': case_no,
                        'source': '厦门法院网',
                    }