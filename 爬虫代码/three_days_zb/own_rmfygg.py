#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-07-04 15:37:29
# Project: rmfygg

from pyspider.libs.base_handler import *
import random
import datetime
import urllib.parse
import pymysql


# 输入企业名称作为关键字搜索
class Handler(BaseHandler):
    # 字段映射
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

    def __init__(self):

        # 1.从数据库中提取需要搜索的企业
        def get_company(self):
            config = {
                'host': '10.1.5.160',
                'port': 3306,
                'user': 'root',
                'password': 'root',
                'database': 'test',
                'charset': 'utf8mb4'
            }
            conn = pymysql.connect(**config)
            cursor = conn.cursor()

            try:
                sql = 'select entname from monitor_ent_list_daily'  # 编写sql语句
                cursor.execute(sql)  # 执行sql语句
                company = cursor.fetchall()  # 得到结果
                return company
                # conn.commit()         # 提交事务
            except:
                conn.rollback()  # 若出错了，则回滚,在没提交之前可以回到sql语句执行之前
            finally:
                conn.close()

        super(Handler, self).__init__()

        # 拿到企业名称
        self.company = get_company(self)

        # 只爬取最近10天的数据
        self.last_day = str(datetime.date.today() - datetime.timedelta(days=10))

        # 用户代理池
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

        # 请求头，为了防止cookies过期，这里没写死
        self.headers = {
            ':authority': 'rmfygg.court.gov.cn',
            ':method': 'POST',
            ':path': '/web/rmfyportal/noticeinfo?p_p_id=noticelist_WAR_rmfynoticeListportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=initNoticeList&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1',
            ':scheme': 'https',
            'accept': ' application/json, text/javascript, */*; q=0.01',
            'accept-encoding': ' gzip, deflate, br',
            'accept-language': ' zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': ' application/x-www-form-urlencoded; charset=UTF-8',
            'origin': ' http://rmfygg.court.gov.cn',
            'referer': ' http://rmfygg.court.gov.cn/web/rmfyportal/noticeinfo',
            'user-agent': ' Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            'x-requested-with': ' XMLHttpRequest',
            'User-Agent': random.choice(self.UA),
        }



    crawl_config = {
        'itag': 'v6.14',  # 代码版本号
        'proxy': 'H67U07LZ5DMU714P:91C4756816F315D4@http-pro.abuyun.com:9010'  # 用户代理
    }

    # 失败重试
    retry_delay = {
        0: 60,
        1: 60 * 1,
        2: 60 * 2,
        3: 60 * 3,
        4: 60 * 4,
        5: 60 * 5,
        6: 60 * 6,
        7: 60 * 7,
        8: 60 * 8,
        9: 60 * 9,
        10: 60 * 10,
        11: 60 * 11,
        12: 60 * 12,
    }

    # 得到cookie
    def get_cookie(self):
        import requests
        url = 'https://rmfygg.court.gov.cn/web/rmfyportal/noticeinfo'
        header = {
            'accept': ' application/json, text/javascript, */*; q=0.01',
            'accept-encoding': ' gzip, deflate, br',
            'accept-language': ' zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': ' http://rmfygg.court.gov.cn',
            'user-agent': ' Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            'x-requested-with': ' XMLHttpRequest',
            'User-Agent': random.choice(self.UA),
        }
        response = requests.get(url, header)
        return response.cookies.get_dict()

    # 将fygg_total_num 结果插入数据库
    def into_mysql(self, fygg_total_num, company):
        config = {
            'host': '10.1.5.160',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'database': 'test',
            'charset': 'utf8mb4'
        }
        conn = pymysql.connect(**config)
        cursor = conn.cursor()

        try:
            sql = 'update monitor_ent_list_daily set fygg_total_num = %s where entname = %s'
            cursor.execute(sql, (fygg_total_num, company))
            conn.commit()

        except:
            conn.rollback()
        finally:
            conn.close()

    @every(minutes=24 * 60)
    @config(age=60 * 60)
    def on_start(self):
        company = self.company
        cookie = self.get_cookie()

        for i in range(len(company)):
            # post 请求参数
            data = {'_noticelist_WAR_rmfynoticeListportlet_content': '',
                    # '_noticelist_WAR_rmfynoticeListportlet_searchContent': urllib.parse.quote('江苏中南建筑产业集团有限责任公司'),
                    '_noticelist_WAR_rmfynoticeListportlet_searchContent': company[i][0],
                    '_noticelist_WAR_rmfynoticeListportlet_IEVersion': 'ie',
                    '_noticelist_WAR_rmfynoticeListportlet_flag': 'click',
                    '_noticelist_WAR_rmfynoticeListportlet_noticeType': '',
                    '_noticelist_WAR_rmfynoticeListportlet_aoData': '[{"name":"sEcho","value":1},{"name":"iColumns","value":6},{"name":"sColumns","value":",,,,,"},{"name":"iDisplayStart","value":0},{"name":"iDisplayLength","value":15},{"name":"mDataProp_0","value":null},{"name":"mDataProp_1","value":null},{"name":"mDataProp_2","value":null},{"name":"mDataProp_3","value":null},{"name":"mDataProp_4","value":null},{"name":"mDataProp_5","value":null}]'
                    }

            # 请求url，为了避免重复链接，在后面加上了#i
            url = 'https://rmfygg.court.gov.cn/web/rmfyportal/noticeinfo?p_p_id=noticelist_WAR_rmfynoticeListportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=initNoticeList&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1#{}'.format(
                i)

            self.crawl(url, headers=self.headers, method='POST', data=data, callback=self.update_mysql, cookies=cookie,
                       save={'company_now': company[i][0], 'page': '0'})

    @config(age=10 * 24 * 60 * 60)
    def update_mysql(self, response):
        company_now = response.save['company_now']
        page = int(response.save['page'])

        # 用于解码json数据
        json_list = response.json['data']
        print(json_list)

        fygg_total_num = int(response.json['iTotalRecords'])
        print(fygg_total_num)
        # 将数据插入数据库
        self.into_mysql(fygg_total_num, company_now)
        print('更新数据成功')

        # 判断有没有检索结果，如果没有结束
        if fygg_total_num == 0:
            print('{}没有检索信息'.format(company_now))
        else:

            # 遍历检索结果之中的所有链接得到详情
            for item in json_list:
                uuid = item.get('uuid', '')
                print(uuid)

                pages = fygg_total_num // 15 + 1  # 每页最多显示15条，由此算出总共几页
                content_url = 'https://rmfygg.court.gov.cn/web/rmfyportal/noticedetail?paramStr=%s' % uuid
                print(content_url)

                header = {
                    ':authority': 'rmfygg.court.gov.cn',
                    ':method': 'GET',
                    ':path': '/web/rmfyportal/noticedetail?paramStr=%s' % uuid,
                    ':scheme': 'https',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                    'cache-control': 'max-age=0',
                    'referer': 'https://rmfygg.court.gov.cn/web/rmfyportal/noticeinfo',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
                }

                url = 'https://rmfygg.court.gov.cn/web/rmfyportal/noticedetail?p_p_id=noticedetail_WAR_rmfynoticeDetailportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=noticeDetail&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1&_noticedetail_WAR_rmfynoticeDetailportlet_uuid=%s' % uuid

                self.crawl(url=url, headers=header, callback=self.detail_page, save={'content_url': content_url,
                                                                                     'fygg_total_num': fygg_total_num
                                                                                     }, cookies=response.cookies)

            # 这里是在爬近10天的，现在我们爬全部的，先注释掉
            '''
            last_date = json_list[-1].get('publishDate','')
            if last_date > self.last_day:
                print('%s 大于 %s'%(last_date,self.last_day))
            '''

            # 第一页里面对应的cookie中page是0，第一页前面已经爬过了，现在从第二页开始
            for page in range(1, pages):
                url = 'https://rmfygg.court.gov.cn/web/rmfyportal/noticeinfo?p_p_id=noticelist_WAR_rmfynoticeListportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=initNoticeList&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1#%s' % str(
                    page)
                data = {'_noticelist_WAR_rmfynoticeListportlet_content': '',
                        '_noticelist_WAR_rmfynoticeListportlet_searchContent': '',
                        '_noticelist_WAR_rmfynoticeListportlet_IEVersion': 'ie',
                        '_noticelist_WAR_rmfynoticeListportlet_flag': 'init',
                        '_noticelist_WAR_rmfynoticeListportlet_noticeType': '',
                        '_noticelist_WAR_rmfynoticeListportlet_aoData': '[{"name":"sEcho","value":5},{"name":"iColumns","value":6},{"name":"sColumns","value":",,,,,"},{"name":"iDisplayStart","value":%s},{"name":"iDisplayLength","value":10},{"name":"mDataProp_0","value":null},{"name":"mDataProp_1","value":null},{"name":"mDataProp_2","value":null},{"name":"mDataProp_3","value":null},{"name":"mDataProp_4","value":null},{"name":"mDataProp_5","value":null}]' % str(
                            (page) * 10)
                        }
                self.crawl(url, headers=self.headers, method='POST', data=data, callback=self.update_mysql,
                           save={'page': page}, cookies=response.cookies)

    @config(priority=4)
    def detail_page(self, response):

        fygg_total_num = response.save['fygg_total_num']
        if response.json:
            ann_content = response.json.get('noticeContent', '')
            ann_type = response.json.get('noticeType', '')
            announcer = response.json.get('court', '')
            defendant = response.json.get('tosendPeople', '')
            noticeCode = response.json.get('noticeCode', '')
            pdf_url = 'https://rmfygg.court.gov.cn/court-service/%s.pdf' % noticeCode
            uuid = response.json.get('uuid', '')
            content_url = 'https://rmfygg.court.gov.cn/web/rmfyportal/noticedetail?paramStr=%s' % uuid
            ann_date = response.json.get('publishDate', '')
            print(ann_date)
            yield {
                'id': '',
                '_id_': '',
                'ann_type': ann_type,
                'announcer': announcer,
                'defendant': defendant,
                'ann_date': ann_date + 'T00:00:00+08:00',
                'ann_content': ann_content,
                'ann_html': ann_content,
                'content_url': content_url,
                'pdf_url': pdf_url,
                'case_no': '',
                'source': '人民法院公告网',
            }
