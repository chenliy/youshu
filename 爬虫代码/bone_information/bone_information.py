#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-06-21 15:07:42
# Project: zq

from pyspider.libs.base_handler import *
import re
import time
from pyquery import PyQuery as pq
import hashlib
import requests


class Handler(BaseHandler):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'www.chinabond.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
    }
    crawl_config = {
        'itag': 'qz_v004',
        'headers': headers
    }

    schema_def = [{"name": "_id_", "type": "string"},
                  {"name": "url", "type": "string"},
                  {"name": "create_time", "type": "string"},
                  {"name": "html", "type": "string"},
                  {"name": "source", "type": "string"},
                  {"name": "name", "type": "string"},
                  {"name": "short_name", "type": "string"},
                  {"name": "bond_code", "type": "string"},
                  {"name": "publish_time", "type": "string"},
                  {"name": "maturity", "type": "string"},
                  {"name": "plan_total_distribution", "type": "string"},
                  {"name": "actual_total_distribution", "type": "string"},
                  {"name": "publisher_short_name", "type": "string"},
                  {"name": "variety", "type": "string"},
                  {"name": "right_of_choice", "type": "string"},
                  {"name": "state_of_interest", "type": "string"},
                  {"name": "frequency", "type": "string"},
                  {"name": "par_interest_rate", "type": "string"},
                  {"name": "bond_rating", "type": "string"},
                  {"name": "subject_rating", "type": "string"},
                  {"name": "bond_rating_agencies", "type": "string"},
                  {"name": "subject_rating_agencies", "type": "string"},
                  {"name": "basic_margin", "type": "string"},
                  {"name": "basic_interest_rate", "type": "string"},
                  {"name": "first_drawing_day", "type": "string"},
                  {"name": "day_of_interest", "type": "string"},
                  {"name": "due_date", "type": "string"},
                  {"name": "circulation_sign", "type": "string"},
                  {"name": "circulation_day", "type": "string"},
                  {"name": "issuing_rate", "type": "string"},
                  {"name": "circulation_place", "type": "string"},
                  {"name": "first_issue_scope", "type": "string"},
                  {"name": "first_issue_price", "type": "string"},
                  {"name": "interest_rate", "type": "string"},
                  {"name": "total_rate", "type": "string"},
                  {"name": "remark", "type": "string"},
                  {"name": "residual_principal_value", "type": "string"}]

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(
            'http://www.chinabond.com.cn/jsp/include/EJB/queryResult.jsp?queryType=0&sType=2&zqdm=&zqjc=&zqxz=00&eYear2=0000',
            callback=self.get_page)

    def get_page(self, response):
        total = int(re.compile(r"&nbsp;当前<span id='nowpage'>.*?</span>/(.*?)页", re.S).findall(response.text)[0])
        page = int((total + 25 - 1) / 25) + 1

        url1 = 'http://www.chinabond.com.cn/jsp/include/EJB/queryResult.jsp?pageNumber={}&queryType=0&sType=2&zqdm=&zqjc=&zqxz=00&eYear2=0000&bigPageNumber={}&bigPageLines=500&zqdmOrder=1&fxrqOrder=1&hkrOrder=1&qxrOrder=1&dqrOrder=1&ssltrOrder=1&zqqxOrder=1&fxfsOrder=1&xOrder=12345678&qxStart=0&qxEnd=0&sWhere=&wsYear=&weYear=&eWhere=&sEnd=0&fxksr=-00-00&fxjsr=-00-00&fxStart=-00-00&fxEnd=-00-00&dfStart=-00-00&dfEnd=-00-00&start=0&zqfxr=&fuxfs=&faxfs=00&zqxs=00&bzbh=&sYear=&sMonth=00&sDay=00&eYear=&eMonth=00&eDay=00&fxStartYear=&fxStartMonth=00&fxStartDay=00&fxEndYear=&fxEndMonth=00&fxEndDay=00&dfStartYear=&dfStartMonth=00&dfStartDay=00&dfEndYear=&dfEndMonth=00&dfEndDay=00&col=28%2C2%2C5%2C33%2C7%2C21%2C11%2C12%2C23%2C25'

        for x in range(1, page):
            url = url1.format((x * 25) - 24, x)
            self.crawl(url, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):

        # length = len(re.compile(r"tArray\[.\]\[1\] = '(.*?)';", re.S).findall(response.text)[0])
        re_total = re.findall(r"tArray\[.*?\]\[1\] = '(.*?)';", response.text, re.S | re.M)
        if re_total:
            for page in re_total:
                if page.strip():
                    url2 = 'http://www.chinabond.com.cn/jsp/include/EJB/queryResultSingle.jsp?zqdm=' + page.strip()

                    self.crawl(url2, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        dict = {}
        p = pq(response.text)
        contain = p('table.p_wenzi_03 > tr > td[align="center"]')  # 字符串
        for z in range(0, len(contain) - 1, 2):
            try:
                dict[contain[z].text] = contain[z + 1].text
            except:
                pass
        str = dict['债券名称'].strip() + dict['债券代码'].strip()
        hl = hashlib.md5()
        hl.update(str.encode(encoding='utf-8'))
        # print(hl.hexdigest())
        return {
            "_id_": hl.hexdigest(),
            "url": response.url,
            'creat_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            'html': response.text,
            'source': '中国债券信息网',
            'name': dict['债券名称'].strip(),
            'short_name': dict['债券简称'].strip(),
            'bond_code': dict['债券代码'].strip(),
            'publish_time': dict['发行日期'].strip(),
            'maturity': dict['债券期限(年/月/日)'].strip(),
            'plan_total_distribution': dict['计划发行总额(亿元)'].strip(),
            'actual_total_distribution': dict['实际发行总额(亿元)'].strip(),
            'publisher_short_name': dict['发行人简称'].strip(),
            'variety': dict['债券品种'].strip(),
            'right_of_choice': dict['选择权'].strip(),
            'state_of_interest': dict['本息状态'].strip(),
            'frequency': dict['付息频率(月)'].strip(),
            'par_interest_rate': dict['票面利率(%)'].strip(),
            'bond_rating': dict['债券评级'].strip(),
            'subject_rating': dict['主体评级'].strip(),
            'bond_rating_agencies': dict['债券评级机构'].strip(),
            'subject_rating_agencies': dict['主体评级机构'].strip(),
            'basic_margin': dict['基本利差(%)'].strip(),
            'basic_interest_rate': dict['基础利率(%)'].strip(),
            'first_drawing_day': dict['首次划款日'].strip(),
            'day_of_interest': dict['起息日'].strip(),
            'due_date': dict['到期日'].strip(),
            'circulation_sign': dict['流通标志'].strip(),
            'circulation_day': dict['上市流通日'].strip(),
            'issuing_rate': dict['发行手续费率(%)'].strip(),
            'circulation_place': dict['流通场所'].strip(),
            'first_issue_scope': dict['首次发行范围'].strip(),
            'first_issue_price': dict['首次发行价格'].strip(),
            'interest_rate': dict['计息方式'].strip(),
            'total_rate': dict['兑付手续费率(%)'].strip(),
            'remark': dict['备注：'].strip(),
            'residual_principal_value': dict['剩余本金值：'].strip()
        }
