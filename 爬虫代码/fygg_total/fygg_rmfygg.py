# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/27 10:42
# Project:
# @Author: ZQJ
# @Email : zihe@yscredit.com

from pyspider.libs.base_handler import *
import random
import datetime

class Handler(BaseHandler):

    def __init__(self):
        super(Handler,self).__init__()
        self.last_day = str(datetime.date.today()-datetime.timedelta(days=10))
        self.UA = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        ]
        self.headers = {
        ':authority': 'rmfygg.court.gov.cn',
        ':method': 'POST',
        ':path': '/web/rmfyportal/noticeinfo?p_p_id=noticelist_WAR_rmfynoticeListportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=initNoticeList&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1',
        ':scheme': 'https',
        'accept':' application/json, text/javascript, */*; q=0.01',
        'accept-encoding':' gzip, deflate, br',
        'accept-language':' zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type':' application/x-www-form-urlencoded; charset=UTF-8',
       # 'cookie':'_gscu_1049835508=02518942vrdxff73; _gscu_125736681=02518942pl5twc73; Hm_lvt_9e03c161142422698f5b0d82bf699727=1522115769; UM_distinctid=16380c18b6448b-0ddc82556c5d13-3961430f-1fa400-16380c18b655f6; CNZZDATA1273632440=2075159441-1526872508-%7C1526878403; JSESSIONID=0A1E2FE081D2DDA7DE9DA968581AF3DF; LFR_SESSION_STATE_20158=1526888510051; tgw_l7_route=fb4686ab27ce2dbeb7cbdd7edefce9f4',
        'origin':' http://rmfygg.court.gov.cn',
        'referer':' http://rmfygg.court.gov.cn/web/rmfyportal/noticeinfo',
        'user-agent':' Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'x-requested-with':' XMLHttpRequest',
        'User-Agent':random.choice(self.UA),
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
                  {"name": "defendant", "type": "string"},
                ]

    crawl_config = {
        'itag': 'v6.14',
        'proxy': 'H67U07LZ5DMU714P:91C4756816F315D4@http-pro.abuyun.com:9010'
    }

    retry_delay = {
        0: 60,
        1: 60*5,
        2: 60*10,
        3: 60*15,
        4: 60*20,
        5: 60*25,
        6: 60*30,
        7: 60*35,
        8: 60*40,
        9: 60*45,
        10: 60*50,
        11: 60*55,
        12: 60*60,
    }

    def get_cookie(self):
        import requests
        url = 'https://rmfygg.court.gov.cn/web/rmfyportal/noticeinfo'
        header = {
        'accept':' application/json, text/javascript, */*; q=0.01',
        'accept-encoding':' gzip, deflate, br',
        'accept-language':' zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'origin':' http://rmfygg.court.gov.cn',
        'user-agent':' Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'x-requested-with':' XMLHttpRequest',
        'User-Agent':random.choice(self.UA),
        }
        response = requests.get(url,header)
        return response.cookies.get_dict()



    @every(minutes= 24 * 60 )
    @config(age= 60 * 60)
    def on_start(self):
        cookie = self.get_cookie()
        url = 'https://rmfygg.court.gov.cn/web/rmfyportal/noticeinfo?p_p_id=noticelist_WAR_rmfynoticeListportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=initNoticeList&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1#1'
        data = {'_noticelist_WAR_rmfynoticeListportlet_content':'',
                '_noticelist_WAR_rmfynoticeListportlet_searchContent': '',
                '_noticelist_WAR_rmfynoticeListportlet_courtParam': '',
                '_noticelist_WAR_rmfynoticeListportlet_IEVersion': 'ie',
                '_noticelist_WAR_rmfynoticeListportlet_flag': 'init',
                '_noticelist_WAR_rmfynoticeListportlet_noticeType': '',
                '_noticelist_WAR_rmfynoticeListportlet_noticeTypeVal': '全部',
                '_noticelist_WAR_rmfynoticeListportlet_aoData': '[{"name":"sEcho","value":%s},{"name":"iColumns","value":6},{"name":"sColumns","value":",,,,,"},{"name":"iDisplayStart","value":%s},{"name":"iDisplayLength","value":15},{"name":"mDataProp_0","value":null},{"name":"mDataProp_1","value":null},{"name":"mDataProp_2","value":null},{"name":"mDataProp_3","value":null},{"name":"mDataProp_4","value":null},{"name":"mDataProp_5","value":null}]'%(16,0)
                   }
        self.crawl(url,headers=self.headers,method='POST',data=data,callback=self.index_page,save={'page':1},cookies=cookie)

    @config(age= 60 * 60)
    def index_page(self, response):
        #解析页面内容
        json_list = response.json['data']
        if json_list:
            page = response.save['page'] + 1
            for item in json_list:
                uuid = item.get('uuid','')
                content_url = 'https://rmfygg.court.gov.cn/web/rmfyportal/noticedetail?paramStr=%s'%uuid
                header = {
                ':authority': 'rmfygg.court.gov.cn',
                ':method': 'GET',
                ':path': '/web/rmfyportal/noticedetail?paramStr=%s'%uuid,
                ':scheme': 'https',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                'cache-control': 'max-age=0',
                #'cookie':'_gscu_1049835508=02518942vrdxff73; _gscu_125736681=02518942pl5twc73; Hm_lvt_9e03c161142422698f5b0d82bf699727=1522115769; UM_distinctid=16380c18b6448b-0ddc82556c5d13-3961430f-1fa400-16380c18b655f6; CNZZDATA1273632440=2075159441-1526872508-%7C1526894684; tgw_l7_route=e022e091c5193c45f5c6d843b7e8352a; JSESSIONID=3E43E6EBAC8A68A6A2BA467547EE54C8; LFR_SESSION_STATE_20158=1526895585090',
                'referer': 'https://rmfygg.court.gov.cn/web/rmfyportal/noticeinfo',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
                            }

                url = 'https://rmfygg.court.gov.cn/web/rmfyportal/noticedetail?p_p_id=noticedetail_WAR_rmfynoticeDetailportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=noticeDetail&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1&_noticedetail_WAR_rmfynoticeDetailportlet_uuid=%s'%uuid
                self.crawl(url=url,headers=header,callback=self.detail_page,save={
                    'content_url':content_url
                },cookies=response.cookies)

            try:
                last_date = json_list[-1].get('publishDate','')
            except:
                last_date = self.last_day
            if last_date > self.last_day:
                print('%s 大于 %s'%(last_date,self.last_day))
                url = 'https://rmfygg.court.gov.cn/web/rmfyportal/noticeinfo?p_p_id=noticelist_WAR_rmfynoticeListportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=initNoticeList&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1#%s'%str(page)
                data = {'_noticelist_WAR_rmfynoticeListportlet_content': '',
                    '_noticelist_WAR_rmfynoticeListportlet_searchContent': '',
                    '_noticelist_WAR_rmfynoticeListportlet_IEVersion': 'ie',
                    '_noticelist_WAR_rmfynoticeListportlet_flag': 'init',
                    '_noticelist_WAR_rmfynoticeListportlet_noticeType':'',
                    '_noticelist_WAR_rmfynoticeListportlet_aoData': '[{"name":"sEcho","value":5},{"name":"iColumns","value":6},{"name":"sColumns","value":",,,,,"},{"name":"iDisplayStart","value":%s},{"name":"iDisplayLength","value":10},{"name":"mDataProp_0","value":null},{"name":"mDataProp_1","value":null},{"name":"mDataProp_2","value":null},{"name":"mDataProp_3","value":null},{"name":"mDataProp_4","value":null},{"name":"mDataProp_5","value":null}]'%str((page-1)*10)
                       }
                self.crawl(url,headers=self.headers,method='POST',data=data,callback=self.index_page,save={'page':page},cookies=response.cookies)



    @config(priority=4)
    def detail_page(self, response):
        if response.json:

            ann_content = response.json.get('noticeContent','')
            ann_type = response.json.get('noticeType','')
            announcer=response.json.get('court','')
            defendant=response.json.get('tosendPeople','')
            noticeCode=response.json.get('noticeCode','')
            pdf_url = 'https://rmfygg.court.gov.cn/court-service/%s.pdf'%noticeCode
            uuid = response.json.get('uuid','')
            content_url = 'https://rmfygg.court.gov.cn/web/rmfyportal/noticedetail?paramStr=%s'%uuid
            ann_date = response.json.get('publishDate','')
            print(ann_date)
            yield {
                'id':'',
                '_id_':'',
                'ann_type':ann_type,
                'announcer':announcer,
                'defendant':defendant,
                'ann_date':ann_date + 'T00:00:00+08:00',
                'ann_content':ann_content,
                'ann_html':ann_content,
                'content_url':content_url,
                'pdf_url':pdf_url,
                'case_no':'',
                'source':'人民法院公告网',
            }