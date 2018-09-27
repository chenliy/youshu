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
import hashlib
import urllib.parse


class Handler(BaseHandler):
    def fun_economic_division(self, code):
        if code == '01':
            return "经济特区"
        elif code == '02':
            return "经济技术开发全区"
        elif code == '03':
            return "高新技术产业开发区"
        elif code == '04':
            return "保税区"
        elif code == '05':
            return "保税区"
        elif code == '06':
            return "保税港区、综合保税区"
        elif code == '07':
            return "保税物流园区"
        elif code == '09':
            return "一般经济区域"
        else:
            return code

    def fun_getTradeType(self, code):
        if code == "10000000":
            return "进出口收发货人"
        elif code == "01000000":
            return "报关企业"
        elif code == "00100000":
            return "报关企业分支机构"
        elif code == "00010000":
            return "特殊监管区双重身份企业"
        elif code == "00000100":
            return "临时注册企业"
        elif code == "00000010":
            return "加工生产企业"
        elif code == "00000001":
            return "保税仓库"
        elif code == "000000001":
            return "进出境运输工具负责人"
        elif code == "00000002":
            return "出口监管仓库"
        elif code == "20000000":
            return "进出口收发货人分支机构"
        else:
            return code

    def fun_getSpecialTradeZone(self, code):
        if code == "3122F941":
            return "外高桥保税区"
        elif code == "3122F972":
            return "外高桥保税物流园区"
        elif code == "3116F963":
            return "洋山保税港区"
        elif code == "3122F964":
            return "浦东机场综合保税区"
        elif code == "3122F295":
            return "陆家嘴金融片区"
        elif code == "3122F296":
            return "上海金桥开发区"
        elif code == "3122F297":
            return "张江高科技片区"
        elif code == "1207F991":
            return "天津港非特殊监管区"
        elif code == "1207F961":
            return "东疆保税港区"
        elif code == "1210F992":
            return "天津机场非特殊监管区"
        elif code == "1207F942":
            return "天津机场保税区空港"
        elif code == "1210F962":
            return "天津机场滨海新区综合保税区"
        elif code == "1207F993":
            return "滨海商务区非特殊监管区"
        elif code == "1207F943":
            return "滨海商务区保税区海港"
        elif code == "1207F973":
            return "滨海商务区保税物流园"
        elif code == "3512F991":
            return "平潭非综合区"
        elif code == "3512F981":
            return "平潭综合实验区"
        elif code == "3501F293":
            return "福州经开区非特殊监管区"
        elif code == "3501F243":
            return "福州保税区"
        elif code == "3501F253":
            return "福州出口加工区"
        elif code == "3501F963":
            return "福州保税港区"
        elif code == "3502F992":
            return "厦门非特殊监管区"
        elif code == "3502F942":
            return "厦门象屿保税区"
        elif code == "3502F972":
            return "象屿保税物流园区"
        elif code == "3502F962":
            return "厦门海沧保税港区"
        elif code == "4403F992":
            return "蛇口非特殊监管区"
        elif code == "4403F962":
            return "蛇口前海保税港区"
        elif code == "4430F991":
            return "南沙新区非特殊监管区"
        elif code == "4430F961":
            return "广州南沙保税港区"
        elif code == "4404F993":
            return "珠海横琴新区"
        elif code == "99999999":
            return "非特殊区域"
        else:
            return code

    def fun_getReport(self, code):
        if code == 0:
            return "正常"
        elif code == 1:
            return "注销"
        else:
            return code

    def fun_rate(self, code):
        if code == 'AA' or code == '0' or code == 'A':
            return '认证企业'
        elif code == 'B':
            return '一般信用企业'
        else:
            return '失信企业'

    schema_def = [{"name": "_id_", "type": "string"},
                  {"name": "url", "type": "string"},
                  {"name": "create_time", "type": "string"},
                  {"name": "html", "type": "string"},
                  {"name": "source", "type": "string"},
                  {"name": "unicode", "type": "string"},
                  {"name": "customs_registration_code", "type": "string"},
                  {"name": "registration_date", "type": "date"},
                  {"name": "organization_code", "type": "string"},
                  {"name": "company_name", "type": "string"},
                  {"name": "registration_customs", "type": "string"},
                  {"name": "address", "type": "string"},
                  {"name": "administrative_division", "type": "string"},
                  {"name": "economic_division", "type": "string"},
                  {"name": "business_category", "type": "string"},
                  {"name": "special_trade_area", "type": "string"},
                  {"name": "category_of_industry", "type": "string"},
                  {"name": "validity_of_customs_declaration", "type": "string"},
                  {"name": "business_type", "type": "string"},
                  {"name": "customs_cancellation_sign", "type": "string"},
                  {"name": "annual_information", "type": "string"},
                  {"name": "abnormality_of_credit", "type": "string"},
                  {"name": "credit_rating", "type": "string"},
                  {"name": "Administrative_sanction", "type": "list"},
                  {"name": "party", "type": "string"},
                  {"name": "case_nature", "type": "string"},
                  {"name": "punishment_date", "type": "date"},
                  {"name": "decision_num", "type": "string"}]

    crawl_config = {
        'itag': 'v001',
    }

    def __init__(self):

        self.headers1 = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
            'Host': 'credit.customs.gov.cn',
            'Origin': 'http://credit.customs.gov.cn'
        }
        self.headers2 = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '44',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Cookie':'JSESSIONID=4uQ0gJm0nRRGOoxj4W8JMJaS_2ZBoT0mzOvTHRzk2-V9LYhhSniT!-912624801',
            'Host': 'credit.customs.gov.cn',
            'Origin': 'http://credit.customs.gov.cn',
            'Referer': 'http://credit.customs.gov.cn/ccppCopAction/queryCop.action',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
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
        resp1 = requests.get(url1, headers=self.headers1, cookies=cookie)
        yundama = YDMHttp(username, password, appid, appkey)
        cid, vcode = yundama.decode_mem(resp1.content, '5006', 10)
        print('vcode:{}'.format(vcode))
        image = Image.open(io.BytesIO(resp1.content))
        image.show()
        # post链接
        url2 = 'http://credit.customs.gov.cn/ccppCopAction/queryCopIn.action'
        # 企业名，轮询，先用佛山市顺德区蓝基恩塑料有限公司代替
        key_word = ['佛山市顺德区蓝基恩塑料有限公司', '快钱支付清算信息有限公司', '中国银联股份有限公司']
        for k in range(len(key_word)):
            key = urllib.parse.quote(key_word[k])
            data = 'copName={}&sf={}&x=46&y=20&randomCode={}'.format(key, sf, vcode)
            html2 = requests.post(url2, data=data, headers=self.headers2, cookies=cookie).text
            # print(html2)
            detail = re.compile("getDetail(.*?);", re.S).findall(html2)
            for i in detail:
                if len(detail) > 20:
                    print("你检索的信息超过20条，请精确您的查询条件")
                    break
                i = eval(i)
                seqNo = i[0]
                saicSysNo = i[1]
                data2 = {'seqNo': i[0],
                         'saicSysNo': i[1]
                         }
                print(data2)
                self.crawl('http://credit.customs.gov.cn/ccppCopAction/getDetail.action', headers=self.headers2,
                           cookies=cookie, data=data2, callback=self.detail_page)
                print(k)

    @config(priority=2)
    def detail_page(self, response):
        url4 = response.url
        # print(response.text)
        create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        html = response.text
        source = '中国海关企业进出口信用信息公示平台'
        specific = response.doc('div#tabs-1 td')
        result_dict = {}
        for i in range(0, len(specific) - 2, 2):
            result_dict[specific[i].text.strip()] = specific[i + 1].text.strip()
        unicode = result_dict.get('统一社会信用代码')
        customs_registration_code = result_dict.get('海关注册编码')
        registration_date = result_dict.get('注册日期')
        organization_code = result_dict.get('组织机构代码')
        company_name = result_dict.get('企业中文名称')
        registration_customs = result_dict.get('注册海关')
        address = result_dict.get('工商注册地址')
        administrative_division = result_dict.get('行政区划')
        category_of_industry = result_dict.get('行业种类')
        validity_of_customs_declaration = result_dict.get('报关有效期')
        business_type = result_dict.get('跨境贸易电子商务类型')
        annual_information = result_dict.get('年报情况')
        abnormality_of_credit = result_dict.get('信用信息异常情况')
        economic_division_num = \
        re.compile('<script>document.write\(getApanage\((.*?)\)\)</script>', re.S).findall(html)[0]
        print(economic_division_num, 1)
        economic_division = self.fun_economic_division(eval(economic_division_num))
        print(economic_division, 2)
        business_category_num = \
        re.compile('<script>document.write\(getTradeType\((.*?)\)\)</script>', re.S).findall(html)[0]
        print(business_category_num, 3)
        business_category = self.fun_getTradeType(eval(business_category_num))
        print(business_category, 4)
        special_trade_area_num = \
        re.compile('<script>document.write\(getSpecialTradeZone\((.*?)\)\)</script>', re.S).findall(html)[0]
        print(special_trade_area_num, 5)
        special_trade_area = self.fun_getSpecialTradeZone(eval(special_trade_area_num))
        print(special_trade_area, 6)
        customs_cancellation_sign_num = \
        re.compile('<script>document.write\(getRevoke\((.*?)\)\)</script>', re.S).findall(html)[0]
        print(customs_cancellation_sign_num, 7)
        customs_cancellation_sign = self.fun_getReport(int(eval(customs_cancellation_sign_num)))
        print(customs_cancellation_sign, 8)
        print(result_dict)
        rate_num1 = re.compile('var pic="(.*?)"', re.S).findall(response.text)[0]
        print(rate_num1, 9)
        credit_rating = self.fun_rate(rate_num1)
        print(credit_rating, 10)
        list = response.doc('table#caseInfo.mainTab2 td')
        if len(list) != 4:
            Administrative_sanction = '没有行政处罚信息'
            party = ''
            case_nature = ''
            punishment_date = ''
            decision_num = ''
        else:
            Administrative_sanction = ''
            party = list[0].text
            case_nature = list[1].text
            punishment_date = list[2].text
            decision_num = list[3].text
        print(Administrative_sanction)
        print(party, 11)
        print(case_nature, 12)
        print(punishment_date, 13)
        print(decision_num, 14)
        str = company_name.strip() + unicode.strip()
        hl = hashlib.md5()
        hl.update(str.encode(encoding='utf-8'))
        url = 'http://credit.customs.gov.cn'
        return {
            "_id_": hl.hexdigest(),
            'url': url,
            'create_time': create_time,
            'html': html,
            'source': source,
            'unicode': unicode,
            'customs_registration_code': customs_registration_code,
            'registration_date': registration_date,
            'organization_code': organization_code,
            'company_name': company_name,
            'registration_customs': registration_customs,
            'address': address,
            'administrative_division': administrative_division,
            'economic_division': economic_division,
            'business_category': business_category,
            'special_trade_area': special_trade_area,
            'category_of_industry': category_of_industry,
            'validity_of_customs_declaration': validity_of_customs_declaration,
            'business_type': business_type,
            'customs_cancellation_sign': customs_cancellation_sign,
            'annual_information': annual_information,
            'abnormality_of_credit': abnormality_of_credit,
            'credit_rating': credit_rating,
            'Administrative_sanction': Administrative_sanction,
            'party': party,
            'case_nature': case_nature,
            'punishment_date': punishment_date,
            'decision_num': decision_num
        }

