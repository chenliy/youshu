#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-12-19 09:32:51
# Project: hospital2

from pyspider.libs.base_handler import *
import logging, re, time
import hashlib
import pymysql
from six import itervalues

'''
class ToMysql():
    def __init__(self, kwargs):

        #kwargs = {  'host':'localhost',
          #          'user':'root',
             #       'passwd':'root',
              #      'db':'others',
              #      'charset':'utf8'}

        hosts = kwargs['host']
        username = kwargs['user']
        password = kwargs['passwd']
        database = kwargs['db']
        charsets = kwargs['charset']

        self.connection = False
        try:
            self.conn = pymysql.connect(host=hosts, user=username, passwd=password, db=database, charset=charsets)
            self.cursor = self.conn.cursor()
            self.cursor.execute("set names " + charsets)
            self.connection = True
        except Exception as e:
            print ("Cannot Connect To Mysql!/n", e)

    def escape(self, string):
        return '%s' % string

    def into(self, tablename=None, **values):

        if self.connection:
            tablename = self.escape(tablename)
            if values:
                values['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

                _keys = ",".join(self.escape(k) for k in values)
                _values = ",".join(['%s', ] * len(values))
                sql_query = "insert into %s (%s) values (%s)" % (tablename, _keys, _values)
            else:
                sql_query = "insert into %s default values" % tablename
            try:
                if values:
                    self.cursor.execute(sql_query, list(itervalues(values)))
                else:
                    self.cursor.execute(sql_query)
                self.conn.commit()
                return True
            except Exception as e:
                print ("An Error Occured: ", e)
                return False



    #获得最新入库的数据
    def _select(self, tablename=None, what="*", where="", offset=0, limit=None,order=False):
        tablename = self.escape(tablename or self.__tablename__)
        if isinstance(what, list) or isinstance(what, tuple) or what is None:
            what = ','.join(self.escape(f) for f in what) if what else '*'

        sql_query = "SELECT %s FROM %s" % (what, tablename)
        if where:
            sql_query += " WHERE %s" % where
        if order:
            sql_query += " order by crawl_time DESC"
        if limit:
            sql_query += " LIMIT %d, %d" % (offset, limit)
        elif offset:
            sql_query += " LIMIT %d, %d" % (offset, limit)

        self.cursor.execute(sql_query)
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
            '''


class Handler(BaseHandler):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Host': 'www.a-hospital.com',
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }
    schema_def = [
        {"name": 'hospital_id', "type": "string"},
        {"name": 'name', "type": "string"},
        {"name": 'address', "type": "string"},
        {"name": 'tel', "type": "string"},
        {"name": 'grade', "type": "string"},
        {"name": 'type', "type": "string"},
        {"name": 'key_department', "type": "string"},
        {"name": 'operation_mode', "type": "string"},
        {"name": 'fax', "type": "string"},
        {"name": 'postal_code', "type": "string"},
        {"name": 'mailbox', "type": "string"},
        {"name": 'website', "type": "string"},
        {"name": 'bus_line', "type": "string"},
        {"name": 'brief_introduction', "type": "string"},
        {"name": 'advanced_equipment', "type": "string"},
        {"name": 'honors', "type": "string"}
    ]

    crawl_config = {
        'itag': 'v1.0.2',
        'headers': headers,
        'time_out': 4000,
        'proxy': 'H21WNK49K6PFSR3P:BF2B9DDE973F0C02@http-pro.abuyun.com:9010'
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

    def get_md5(self, s):
        """get md5 value
        Args
            s: a bytes, can be None
        Returns
            h.hexdigest(): md5(s) value, 32 bit.
        """
        if isinstance(s, str):  # 如果是字符串，那么就用utf-8编码
            s = bytes(s, encoding='utf-8')
        if s:  # 将编码后的s加密
            h = hashlib.md5()
            h.update(s)
            return h.hexdigest()
        else:
            return ''

    @every(minutes=30 * 24 * 60)
    def on_start(self):
        print('hahhhaha')
        url = 'http://www.a-hospital.com/w/%E5%85%A8%E5%9B%BD%E5%8C%BB%E9%99%A2%E5%88%97%E8%A1%A8'
        self.crawl(url, callback=self.get_lists, retries=12)

    @config(age=10 * 24 * 60 * 60)
    def get_lists(self, response):
        for each in response.doc('a[href^="http"]').items():
            url = each.attr.href
            if url.endswith('%E5%88%97%E8%A1%A8') and '/w/' in url:
                self.crawl(url + '#details', callback=self.get_details, retries=12)
                self.crawl(url, callback=self.get_lists, retries=12)

    @config(priority=4)
    def get_details(self, response):
        html = response.etree
        urls = html.xpath('//div[@id="bodyContent"]/ul/li/b/a/@href')
        base_url = 'http://www.a-hospital.com'
        for _ in urls:
            url = base_url + _
            self.crawl(url, callback=self.get_detail, retries=12)
            # for each in response.doc('a[href^="http"]').items():
            #     url = each.attr.href
            # if url.endswith('%E5%8C%BB%E9%99%A2'):
            #     self.crawl(url+'#detail', callback=self.get_detail)
            # if re.findall(r'/w/.*',url) and ('%E5%88%97%E8%A1%A8' not in url):
            #     self.crawl(url+'#detail', callback=self.get_detail)

    @config(priority=6)
    def get_detail(self, response):
        name = ''
        address = ''
        tel = ''
        grade = ''
        _type = ''
        key_department = ''
        operation_mode = ''
        fax = ''
        postal_code = ''
        mailbox = ''
        website = ''
        bus_line = ''
        brief_introduction = ''
        advanced_equipment = ''
        honors = ''

        try:
            html = response.etree
            name = html.xpath('//h1/text()')[0]

            # isHospital = ('医院' in name) or ('中心' in name) or ('研究院' in name) or ('卫生所' in name) or ('卫生院' in name)

            # if not isHospital:
            #     return

            logging.info('判断是否有目录')  # 用来判断是否是一个医院的类，还有没有子医院
            hasColumns = html.xpath('//table[@id="toc"]')
            if not hasColumns:
                logging.info('无目录')  # 这里具体到了每个医院
                texts = html.xpath('//div[@id="bodyContent"]/h2//text()|//div[@id="bodyContent"]/p//text()')
                texts = [text.strip() for text in texts if text.strip()]
                logging.info(texts)
                h_text = html.xpath('//div[@id="bodyContent"]/h2//text()')[0]
                brief_introduction = ''.join(texts[:texts.index(h_text)])
                logging.info(brief_introduction)
                hospital_id = self.get_md5(name + address)
                if brief_introduction or website:
                    yield {
                        'hospital_id': hospital_id,
                        'name': name,
                        'address': address,
                        'tel': tel,
                        'grade': grade,
                        'type': _type,
                        'key_department': key_department,
                        'operation_mode': operation_mode,
                        'fax': fax,
                        'postal_code': postal_code,
                        'mailbox': mailbox,
                        'website': website,
                        'bus_line': bus_line,
                        'brief_introduction': brief_introduction,
                        'advanced_equipment': advanced_equipment,
                        'honors': honors,
                    }
            else:  # 这里还是一类医院，还可以继续细分
                results = html.xpath('//div[@id="bodyContent"]/ul[1]/li')
                d = {}
                for result in results:
                    key, value = ''.join(result.xpath('.//text()')).split('：')[0], ''.join(
                        ''.join(result.xpath('.//text()')).split('：')[1:])
                    d[key] = value
                logging.info(d)
                address = d.get('医院地址', '')
                tel = d.get('联系电话', '')
                grade = d.get('医院等级', '')
                _type = d.get('医院类型', '')
                key_department = d.get('重点科室', '')
                operation_mode = d.get('经营方式', '')
                fax = d.get('传真号码', '')
                postal_code = d.get('邮政编码', '')
                mailbox = d.get('电子邮箱', '')
                website = d.get('医院网站', '')
                # bus_line = d.get('乘车路线','')
                # brief_introduction = d.get('医院概况','')
                # advanced_equipment = d.get('先进设备说明','')
                # honors = d.get('所获荣誉','')
                texts = html.xpath('//div[@id="bodyContent"]/h2//text()|//div[@id="bodyContent"]/p//text()')
                texts = [text.strip() for text in texts if text.strip()]
                logging.info(texts)
                # 目录
                # '医院特色', '服务项目', '医院大事记', '医院专家'
                catalogs = html.xpath('//div[@id="bodyContent"]/h2//text()')
                catalogs = [catalog.strip() for catalog in catalogs if catalog.strip()]
                logging.info(catalogs)
                for i in range(len(catalogs)):
                    if i + 1 < len(catalogs):
                        begin = texts.index(catalogs[i])
                        end = texts.index(catalogs[i + 1])
                        # logging.info(begin)
                        # logging.info(end)
                        # logging.info(texts[begin+1:end])
                        if '概况' in catalogs[i] or '简介' in catalogs[i]:
                            brief_introduction = ''.join(texts[begin + 1:end])
                        if '路线' in catalogs[i]:
                            bus_line = ''.join(texts[begin + 1:end])
                        if '设备' in catalogs[i]:
                            advanced_equipment = ''.join(texts[begin + 1:end])
                        if '荣誉' in catalogs[i]:
                            honors = ''.join(texts[begin + 1:end])
                if brief_introduction or website:
                    hospital_id = self.get_md5(name + address)
                    yield {
                        'hospital_id': hospital_id,
                        'name': name,
                        'address': address,
                        'tel': tel,
                        'grade': grade,
                        'type': _type,
                        'key_department': key_department,
                        'operation_mode': operation_mode,
                        'fax': fax,
                        'postal_code': postal_code,
                        'mailbox': mailbox,
                        'website': website,
                        'bus_line': bus_line,
                        'brief_introduction': brief_introduction,
                        'advanced_equipment': advanced_equipment,
                        'honors': honors,
                    }

        except Exception as e:
            logging.info(e)

    '''
    def on_result(self,result):
        if not result:
            return
        kwargs = {
            'host': '10.1.2.89',
            # 'host': '127.0.0.1',
            'user': 'root',
            # 'passwd': '',
            'passwd': 'ys901',
            'db': 'test',
            'charset': 'utf8'
        }
        # kwargs = {
        #     'host': '10.1.1.40',
        #     'user': 'wangfeng',
        #     'passwd': 'V42OVF6XbVvkwUp',
        #     'db': 'court_announcement',
        #     'charset': 'utf8'
        # }
        sql = ToMysql(kwargs)
        sql.into(tablename='hospital',**result)
        '''
