#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-06-26 15:11:29
# Project: hg

from pyspider.libs.base_handler import *
import re
import requests
from PIL import Image
from yundama import YDMHttp
import io
import time
from pyquery import PyQuery as pq

class Handler(BaseHandler):
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
        'Host':'credit.customs.gov.cn',
        'Origin':'http://credit.customs.gov.cn'
    }
    crawl_config = {
        'itag': 'v001',
        'headers':headers,
               }
    def __init__(self):
        self.headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
        'Host':'credit.customs.gov.cn',
        'Origin':'http://credit.customs.gov.cn'
    }


    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://credit.customs.gov.cn', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        cookie = response.cookies
        sf = re.compile(r'value="(.\d*?)"/>').findall(response.text)[0]
        print('sf等于{}'.format(sf))
        url1 = 'http://credit.customs.gov.cn/ccppCopAction/createImage.action'
        username = 'yscredit'
        password = 'ys@123456'
        appid = '4934'
        appkey = 'b7132447f5d2b263a61cd4252fd01d6a'
        resp1 = requests.get(url1,headers=self.headers,cookies=cookie)
        yundama = YDMHttp(username, password, appid, appkey)
        cid, vcode = yundama.decode_mem(resp1.content, '5006', 10)
        print('vcode:{}'.format(vcode))
        image = Image.open(io.BytesIO(resp1.content))
        #image.show()
        #post链接
        url2 = 'http://credit.customs.gov.cn/ccppCopAction/queryCopIn.action'
        #企业名，轮询，先用佛山市顺德区蓝基恩塑料有限公司代替
        data = 'copName=%E5%BF%AB%E9%92%B1%E6%94%AF%E4%BB%98%E6%B8%85%E7%AE%97%E4%BF%A1%E6%81%AF%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&sf={}&x=46&y=20&randomCode={}'.format(sf,vcode)
        html2 = requests.post(url2,data=data,headers=self.headers,cookies=cookie).text
        print(len(html2))

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
