#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/31 15:48
# Project:
# @Author: ZQJ
# @Email : zihe@yscredit.com

from pyspider.libs.base_handler import *
import re
import subprocess
import os
import requests


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
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'lyzy.jlsfy.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'}

    def download_parse(self, filename, content):
        try:

            with open(filename, 'wb') as f:
                f.write(content)

            output = subprocess.check_output(["antiword", filename])
            text = output.decode('utf-8', 'ignore')
            return text
        except Exception as e:
            print(e)
        finally:
            os.remove(filename)

    @every(minutes=24 * 60)
    def on_start(self):
        for i in range(1, 7):
            url = 'http://lyzy.jlsfy.gov.cn/jxjsajgs/index_{}.jhtml'.format(i)
            self.crawl(url, headers=self.headers, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):

        cookies = response.cookies
        print(1)
        urls = []
        titles = []
        for each in response.doc('ul.organList a[href]').items():
            print(each.attr['href'])
            if 'index' not in each.attr['href']:
                urls.append(each.attr['href'])
                titles.append(each.text)
        times = []
        for each in response.doc('ul.organList div.date').items():
            times.append(each.text())
        print(len(times))
        print(len(urls))
        if len(urls) == len(times) == len(titles):
            for i in range(len(urls)):
                self.crawl(urls[i], callback=self.detail_page, save={'title': titles[i], 'ann_date': times[i]},
                           cookies=cookies, fetch_type='js')

    @config(priority=2)
    def detail_page(self, response):

        title = response.save['title']
        ann_date = response.save['ann_date']
        ann_type = '减刑假释'

        pdf_url = response.doc('#attach0').attr['href']
        print(pdf_url)
        if pdf_url:

            html = requests.get(pdf_url, headers=self.headers).content
            filename = response.doc('a#attach0').text()
            text = self.download_parse(filename=filename, content=html)

            ann_html = text.replace(' ', '').replace('\u3000', '').replace('\xa0', '')
            if '\n' in text:
                ann_content_list = text.split('\n')
            else:
                ann_content_list = text.split(' ')
            ann_content = str(
                [x.strip().replace(' ', '').replace('\u3000', '').replace('\xa0', '') for x in ann_content_list if
                 x.strip()])


        else:
            pdf_url = ''
            ann_content = response.doc('div.sswy_article_m').text()
            ann_html = response.doc('div.sswy_article_t').text() + ':' + ann_content

            if '\n' in ann_content:
                ann_content_list = ann_content.split('\n')
            else:
                ann_content_list = ann_content.split(' ')

        ann_content_list = [x.strip().replace(' ', '').replace('\u3000', '').replace('\xa0', '') for x in
                            ann_content_list if x != '']

        # 优先在标题里面找案号，标题里面没有案号在正文里面找，爬正文里面匹配出岔子
        try:
            # 这里还需要判断的是：有几个案号写一起的情况：将案号分开，正文公用
            # 多少多少号之一也就算了；居然有123之一号这种鬼情况
            case_no = re.compile(r'\(?\d{4}\)?.*?\d号', re.S).findall(title.replace('之一', ''))[0]
            case_no_list = case_no.split('、')


        except:
            try:
                case_no = re.compile(r'\(?\d{4}\)?.*?\d号', re.S).findall(ann_content)[0]
                case_no_list = case_no.split('、')
            except:
                case_no = ''
                case_no_list = []

        defendant = ''
        for x in ann_content_list:
            defendant_list = re.compile(r'罪犯(.*?)[,，:：.。]').findall(x)
            if defendant_list:
                defendant = str(defendant_list[0].split('、'))
                break

        content_url = response.url
        # print(content_url)
        print(case_no_list)
        if case_no_list:
            print(1, ann_type, 3, defendant, 4, ann_date, 5, ann_content, 6, ann_html, 7, content_url, 8, pdf_url, 9,
                  case_no)
            for i in range(len(case_no_list)):
                if i == 0:
                    if '号' not in case_no_list[0][-1]:
                        case_no = case_no_list[0] + '号'
                    else:
                        case_no = case_no_list[0]
                else:
                    num = re.compile(r'\d+$', re.S).findall(case_no_list[0])[0]
                    case_no = case_no_list[0].replace(num, case_no_list[i]) + '号'
                yield {
                    'id': '',
                    '_id_': '',
                    'ann_type': ann_type,
                    'announcer': '辽源市中级人民法院司法公开网',
                    'defendant': defendant,
                    'ann_date': ann_date,
                    'ann_content': ann_content,
                    'ann_html': ann_html,
                    'content_url': content_url,
                    'pdf_url': pdf_url,
                    'case_no': case_no,
                    'source': '辽源市中级人民法院司法公开网',
                }
        else:
            print(1, ann_type, 3, defendant, 4, ann_date, 5, ann_content, 6, ann_html, 7, content_url, 8, pdf_url, 9,
                  case_no)
            yield {
                'id': '',
                '_id_': '',
                'ann_type': ann_type,
                'announcer': '辽源市中级人民法院司法公开网',
                'defendant': defendant,
                'ann_date': ann_date,
                'ann_content': ann_content,
                'ann_html': ann_html,
                'content_url': content_url,
                'pdf_url': pdf_url,
                'case_no': case_no,
                'source': '辽源市中级人民法院司法公开网',
            }

