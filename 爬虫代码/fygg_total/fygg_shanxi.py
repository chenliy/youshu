#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/30 16:53
# Project:
# @Author: ZQJ
# @Email : zihe@yscredit.com


from pyspider.libs.base_handler import *
from lxml import etree
import re
import logging
from datetime import datetime
import hashlib
import json
import requests

# 陕西-送达公告

# 日志输出等级
logging.basicConfig(level=logging.info)


class Handler(BaseHandler):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Host': 'www.gd.xinhuanet.com'
    }

    crawl_config = {
        'itag': 'v5.3',
        'headers': headers,
        'time_out': 10000,
        # 'proxy': 'H14LXDJ6O07CAFDP:150D24D434AC09EE@proxy.abuyun.com:9010'
    }

    retry_delay = {
        0: 60,
        1: 60 * 5,
        2: 60 * 10,
        3: 60 * 15,
        4: 60 * 20,
        5: 60 * 25,
        6: 60 * 30,
        7: 60 * 35,
        8: 60 * 40,
        9: 60 * 45,
        10: 60 * 50,
        11: 60 * 55,
        12: 60 * 60,
    }

    def escape(self, string):
        return '%s' % string

    def parse_time(self, t):
        t = list(t)
        d = {'零': '0', '一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9',
             '○': '0', 'Ｏ': '0', '年': '-', '月': '-', '日': '-', '元': '1', '〇': '0', 'Ο': '0', '０': '0',
             'О': '0', '0': '0', 'O': '0', 'o': '0'
             }
        for i in range(len(t)):
            if t[i] in d.keys():
                t[i] = d[t[i]]
        # 处理汉字为十的情况
        if '十' in t:
            for i in range(len(t)):
                if t[i] == '十':
                    if (i - 1) >= 0 and t[i - 1].isalnum():
                        t[i] = '0'
                    if (i + 1) < len(t) and t[i + 1].isalnum():
                        t[i] = '1'
                    if (i - 1) >= 0 and (i + 1) < len(t) and t[i - 1] == '-' and t[i + 1] == '-':
                        t[i] = '10'
                    if (i - 1) >= 0 and (i + 1) < len(t) and t[i - 1].isalnum() and t[i + 1].isalnum():
                        t[i] = ''
        t = ''.join(t)
        t = re.findall(r'(.{4}[-年\.].{1,2}[-月\.].{1,3}?)[-上下日号\s]', t)[0]
        t = datetime.strptime(t, "%Y-%m-%d").strftime('%Y-%m-%dT00:00:00+08:00')
        return t

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
                  {"name": "defendant", "type": "string"},
                  ]

    def get_md5(self, s):
        """get md5 value
        Args
            s: a bytes, can be None
        Returns
            h.hexdigest(): md5(s) value, 32 bit.
        """
        if isinstance(s, str):
            s = bytes(s, encoding='utf-8')
        if s:
            h = hashlib.md5()
            h.update(s)
            return h.hexdigest()
        else:
            return ''

    @every(minutes=24 * 60)
    @config(age=60 * 60)
    def on_start(self):
        ccs = ['R00', 'R1_', 'R2_', 'R3_', 'R4_', 'R5_', 'R6_', 'R7_', 'R8_', 'R9_', 'RA_', 'RB_']
        for cc in ccs:
            url = 'http://www.sxgaofa.cn/sxgzfww/R00/ggsd_listAjxx.shtml#start#{}'.format(cc)
            data = {
                'fydm': cc,
                'ahqcOrdsr': ''
            }
            self.crawl(url, data=data, method='POST', callback=self.get_lists)

    @config(age=60 * 60)
    def get_lists(self, response):
        try:
            html = etree.HTML(response.text)
            results = html.xpath('//table[@class="mytable"]//tr')
            print(result)
            url = 'http://www.sxgaofa.cn/sxgzfww/R00/ggsd_pjggsd.shtml'
            print(url)
            for result in results:
                list_response = etree.tounicode(result)
                tmp = result.xpath('.//a/@onclick')[0]
                tmp = re.findall(r'tzpjgg(\(.*\))', tmp)[0]
                tmp = list(eval(tmp))
                logging.info(tmp)
                if len(tmp) == 7:
                    ahqc, dybg, dyyg, laaymc, fymc, fbrq, fydm = tmp
                    url = 'http://www.sxgaofa.cn/sxgzfww/R00/ggsd_pjggsd.shtml?ahqc={}&dybg={}&dyyg={}&laaymc={}&fymc={}&ajxx.fbrq={}&ajxx.fydm={}'.format(
                        ahqc, dybg, dyyg, laaymc, fymc, fbrq, fydm)
                    self.crawl(url, callback=self.get_detail,
                               save={'list_response': list_response, 'ahqc': ahqc, 'dybg': dybg, 'fymc': fymc,
                                     'fbrq': fbrq}, retries=12, allow_redirects=False)
        except Exception as e:
            logging.info(e)
            logging.info('当前法院无内容...')

    @config(age=60 * 60)
    @catch_status_code_error
    def get_detail(self, response):
        # 初始化字段
        ann_type = '送达公告'
        announcer = ''
        defendant = ''
        defendant_origin = ''
        ann_date = ''
        ann_content = ''
        ann_html = ''
        content_url = response.url
        pdf_url = ''
        case_no = ''
        source = '陕西法院诉讼服务网'

        list_response = response.save['list_response']
        ahqc = response.save['ahqc']
        dybg = response.save['dybg']
        fymc = response.save['fymc']
        fbrq = response.save['fbrq']
        # html = response.etree
        if response.status_code == 200:
            try:
                html = etree.HTML(response.text)
                detail = html.xpath('//form[@id="form1"]')[0]
                ann_html = etree.tounicode(detail)
                # logging.info('开始结构化..')
                results = html.xpath('//form[@id="form1"]//text()')
                results = [result.strip() for result in results if result.strip()]
                logging.info(results)
                ann_time = fbrq
                ann_date = re.findall(r'(.{4}[-年\.].{1,2}[-月\.].{1,3}?)', ann_time)[0]
                ann_date = datetime.strptime(ann_date, "%Y-%m-%d").strftime('%Y-%m-%dT00:00:00+08:00')
                # if len(results) >= 6:
                # ann_content = ''.join(results)
                announcer = fymc
                defendant_origin = dybg
                for result in results:
                    if dybg in result:
                        if not ann_content:
                            ann_content = ''.join(results[results.index(result) + 1:])
                            case_no = re.findall(r'[(（][1１２2].{3}[）)].{0,8}[刑民行赔执访认送调管脏移引惩保].{2,18}号', ann_content)[
                                0] if re.findall(r'[(（][1１２2].{3}[）)].{0,8}[刑民行赔执访认送调管脏移引惩保].{2,18}号',
                                                 ann_content) else case_no
                            if '、' in defendant_origin:
                                defendants = defendant_origin.split('、')
                            elif ',' in defendant_origin:
                                defendants = defendant_origin.split(',')
                            else:
                                defendants = [defendant_origin]

                            yield {
                                'ann_type': ann_type,
                                'announcer': announcer,
                                'defendant': str(defendants),
                                'ann_date': ann_date,
                                'ann_content': ann_content,
                                'ann_html': ann_html,
                                'content_url': content_url,
                                'pdf_url': pdf_url,
                                'source': source,
                                'case_no': case_no,
                                'id': '',
                                '_id_': ''
                            }
            except Exception as e:
                logging.warning('哪里可能出问题了...')
                logging.warning(e)
