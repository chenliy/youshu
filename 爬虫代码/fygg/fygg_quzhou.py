#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/8/1 19:10
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com
from pyspider.libs.base_handler import *
import re
import requests
import pandas as pd
import os
from math import isnan
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
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.qzzjfy.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'}

    def download_parse(self, filename, content):
        try:
            with open(filename, 'wb') as f:
                f.write(content)

            try:
                data = pd.read_excel(r'C:\Users\ll\Desktop\2.xls', header=None)
            except:
                try:
                    data = pd.read_excel(r'C:\Users\ll\Desktop\2.xlsx', header=None)
                except:
                    data = ''
                    print('有误')

            return data
        except Exception as e:
            print(e)
        finally:
            os.remove(filename)

    @every(minutes=24 * 60)
    def on_start(self):
        for i in range(1, 17):
            url = 'http://www.qzzjfy.gov.cn/?cat=5&paged={}'.format(i)
            self.crawl(url, headers=self.headers, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        cookies = response.cookies
        urls = []
        times = []
        titles = []
        for each in response.doc('ul.archive-list.inews.icon li a[href]').items():
            urls.append(each.attr['href'])
            titles.append(each.text())
        for each in response.doc('span.xg-fr').items():
            times.append(each.text())
        if len(urls) == len(times) == len(titles):
            for i in range(len(urls)):
                self.crawl(urls[i], headers=self.headers, cookies=cookies,
                           save={'title': titles[i], 'ann_date': times[i]}, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):


        #有两种情况1是网页中是excle 文件，二是直接是表格
        a = re.compile('\d{1,4}', re.S).findall(response.save['ann_date'])
        ann_date = '-'.join(a)

        pdf_url = response.doc('div.entry-content p a[href]').attr['href']

        #如果是附件
        if pdf_url:

            html = requests.get(pdf_url, headers=self.headers).content
            filename = response.doc('div.entry-content p a[href]').text()

            #写入文件后再读出
            data = self.download_parse(filename=filename, content=html)

            #文件标题
            title = data.iloc[0, 0].replace(' ', '').replace('\u3000', '').replace('\xa0', '')

            #处理标题单元格合并的情况
            list1 = []
            list2 = []
            for j in range(len(data.columns)):
                list1.append(data.iloc[1, j])
                list2.append(data.iloc[2, j])

            for i in range(len(list2)):
                try:
                    if isnan(list2[i]):
                        list2[i] = list1[i]
                except:
                    pass

            result_total = []

            #将每一行数据写入列表中，大列表中的每一个小列表是一个字段
            for i in range(3, len(data.index)):
                result = []
                for j in range(len(data.columns)):
                    result.append(data.iloc[i, j])

                result_total.append(result)

            for i in range(len(result_total)):
                print(result_total[i])
                print(list2)

                #每一个小列表构成一个字典作为内容
                if len(list2) == len(result_total[i]):
                    content = {}
                    for j in range(len(list2)):
                        content[list2[j]] = result_total[i][j]
                else:
                    print('形式有错误')
                    break

                ann_content = content
                ann_type = '减刑假释公告'
                defendant = ann_content.get('罪犯姓名', '')
                ann_html = ann_content
                ann_html['title'] = title

                content_url = response.url
                case_no = ''

                print(1, ann_type, 3, defendant, 4, ann_date, 5, ann_content, 6, ann_html, 7, content_url, 8, pdf_url,
                      9,
                      case_no)

                yield {
                    'id': '',
                    '_id_': '',
                    'ann_type': ann_type,
                    'announcer': '衢州市中级人民法院网',
                    'defendant': defendant,
                    'ann_date': ann_date,
                    'ann_content': str(ann_content),
                    'ann_html': str(ann_html),
                    'content_url': content_url,
                    'pdf_url': pdf_url,
                    'case_no': case_no,
                    'source': '衢州市中级人民法院网',
                }
        #如果是直接网页的情况
        if not pdf_url:
            pdf_url = ''
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            trs = soup.find_all('tr')
            result_total = []

            #遍历每一个标签
            for tr in trs:
                result = []
                for td in tr:
                    result.append(td.string)
                result_total.append(result)

            #去掉标签里面‘\n’的干扰
            b = []
            for x in result_total:
                a = []
                for y in x:
                    if y != '\n':
                        a.append(y)
                b.append(a)

            for i in range(len(b)):
                if len(b[i]) == len(b[-1]):
                    title = b[i]
                    try:
                        print(1111, int(title[0])) #如果不是数字的话就会报错,说明匹配到的不是标题行,如果不报错标题行和内容行并不是一一对应的
                        title = range(20) #能力有限，列键弄不灵清了，用0-19作为列键
                        break

                    except:
                        #报错了，说明匹配到的列键和内容一一对应
                        for i in range(len(title)):
                            try:
                                if not title[i]:
                                    title[i] = '考核期(月)' #这个特殊，读出来这个位置居然是none ，改回‘考核期’
                            except:
                                pass
                        print(title)
                        break
            #构成字典
            for i in range(len(b)):
                content = {}
                for k in range(len(b[i])):
                    content[title[k]] = b[i][k]

                ann_content = content
                ann_type = '减刑假释公告'
                defendant = ann_content.get('罪犯姓名', '')
                ann_html = ann_content

                content_url = response.url
                case_no = ''

                print(1, ann_type, 3, defendant, 4, ann_date, 5, ann_content, 6, ann_html, 7, content_url, 8, pdf_url,
                      9,
                      case_no)
                yield {
                    'id': '',
                    '_id_': '',
                    'ann_type': ann_type,
                    'announcer': '衢州市中级人民法院网',
                    'defendant': defendant,
                    'ann_date': ann_date,
                    'ann_content': str(ann_content),
                    'ann_html': str(ann_html),
                    'content_url': content_url,
                    'pdf_url': pdf_url,
                    'case_no': case_no,
                    'source': '衢州市中级人民法院网',
                }






















