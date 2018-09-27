#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/30 16:53
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

from pyspider.libs.base_handler import *
import re
import requests
import subprocess
import os


class Handler(BaseHandler):
    crawl_config = {
        'itag': 'v7.31',
        'time_out': 100000,
        # 'proxy': 'H67U07LZ5DMU714P:91C4756816F315D4@http-pro.abuyun.com:9010'

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
            'Host': 'kmzy.ynfy.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
        }

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
        for i in range(1, 210):
            url = 'http://kmzy.ynfy.gov.cn/fygg/index_{}.jhtml'.format(i)
            self.crawl(url, callback=self.index_page, headers=self.headers)

    @config(age=60 * 60)
    def index_page(self, response):
        cookies = response.cookies

        urls = []
        times = []
        titles = []

        for each in response.doc('ul.sswy_news div.c1-body li a[href]').items():
            urls.append(each.attr['href'])
            titles.append(each.text())
        for each in response.doc('li div.date').items():
            times.append(each.text())

        if len(urls) == len(times):
            for i in range(len(urls)):
                self.crawl(urls[i] + '#{}'.format(i), callback=self.detail_page,
                           save={'ann_date': times[i], 'title': titles[i]}, cookies=cookies)

    @config(priority=2)
    def detail_page(self, response):
        ann_date = response.save['ann_date'].split(' ')[0] + 'T00:00:00+08:00'
        print(ann_date)

        title = response.save['title']

        # 由于发现明明是在送达公告一栏，却仍然有其他类型的公告，由此根据库里的现有字段，进行判断：
        type_list = ['起诉状副本及开庭传票', '裁判文书', '送达公告', '执行文书', '起诉状、上诉状副本', '开庭传票', '减刑假释', '更正', '宣告失踪、死亡', '破产文书']
        if '裁判' in title:
            ann_type = '裁判文书'
        elif '起诉状' in title or '上诉状' in title:
            ann_type = '起诉状、上诉状副本'
        elif '执行' in title:
            ann_type = '执行文书'
        elif '开庭传票' in title:
            ann_type = '开庭传票'
        elif '减刑' in title or '假释' in title:
            ann_type = '减刑假释'
        else:
            ann_type = '送达文书'

        # 这里要先判断正文是不是一个链接
        docx = response.doc('div.sswy_article_box a[href]').attr['href']

        if docx and '.doc' in docx:

            pdf_url = docx
            url = docx
            html = requests.get(url, headers=self.headers).content

            filename = response.doc('div.sswy_article_box a[href]').text()

            text = self.download_parse(filename=filename, content=html)

            ann_html = text.replace(' ', '').replace('\u3000', '').replace('\xa0', '')

            ann_content_list = text.split('\n')
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
        print(ann_content_list)
        for i in range(len(ann_content_list)):
            if ann_content_list[i][-1] in [':', '：']:
                print(2)
                defendant = str(ann_content_list[i][:-1].split('、'))
                if eval(defendant) == ['']:
                    print(1)
                    defendant = str(ann_content_list[i - 1].split('、'))

                if not defendant:
                    print(1)
                    defendant = str(ann_content_list[i - 1].split('、'))
            if defendant:
                break

        content_url = response.url
        # print(content_url)

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
                    'announcer': '昆明市中级人民法院',
                    'defendant': defendant,
                    'ann_date': ann_date,
                    'ann_content': ann_content,
                    'ann_html': ann_html,
                    'content_url': content_url,
                    'pdf_url': pdf_url,
                    'case_no': case_no,
                    'source': '昆明市中级人民法院',
                }