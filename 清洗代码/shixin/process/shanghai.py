import os
import sys
sys.path.append(os.path.abspath(__file__ + "/../../../../"))
from IKEA.shixin.process.base_process import Base
from IKEA.mysql.mysqlbase import MysqlBase
from IKEA.shixin.config import connecter
from pyquery import PyQuery as pq
from datetime import datetime
import json
import re

def extract_business_entity(s):
    if '法定代表人' in s:
        l = s.rfind('（')
        r = s.rfind('）')
        if l != -1 and r != -1:
            t = s.rfind('：')
            name = s[:l]
            business_entity = s[t+1:r]
            return name, business_entity
    else:
        return s, ''

class ShangHai(Base):

    def wjzxssaj(self):
        print('{}:{}'.format(datetime.now(), self.path))
        d = pq(self.detail)
        name, case_code = eval(self.list)['bt'].split('，')
        key_msg = [each.text() for n, each in enumerate(d(".tdnr").items()) if n % 2 == 0]
        value_msg = [each.text() for n, each in enumerate(d(".tdnr").items()) if n % 2 != 0]
        msg = dict(zip(key_msg, value_msg))
        msg = msg if msg else {'被执行人': name, '案号': case_code}
        release_date = re.findall('<strong>(20.*?)</strong>', self.detail)[0] if re.findall('<strong>(20.*?)</strong>', self.detail) else ''
        court_name, phone = tuple(msg.get('承办法院、联系电话').split('  ')) if msg.get('承办法院、联系电话').split('  ') else ['', '']
        limiting_cause = d('.nr').not_('[align="center"]').text()
        name, business_entity = extract_business_entity(msg['被执行人'])
        self.exposure_desk['name'] = name
        self.exposure_desk['business_entity'] = business_entity
        self.exposure_desk['case_code'] = msg.get('案号')
        self.exposure_desk['court_name'] = court_name
        self.exposure_desk['execute_money'] = msg.get('执行标的金额（元）')
        self.exposure_desk['release_date'] = msg.get('发布日期')
        self.exposure_desk['address'] = msg.get('被执行人地址')
        self.exposure_desk['tel_of_court'] = phone
        self.exposure_desk['execution_applicant'] = msg.get('申请执行人')
        self.exposure_desk['release_date'] = release_date
        self.exposure_desk['limiting_cause'] = limiting_cause
        super().split_ex()

    def xzgxf(self):
        return self.wjzxssaj()

    def xzcj(self):
        return self.wjzxssaj()

    def xztzb(self):
        return self.wjzxssaj()

    def wszc(self):
        return self.wjzxssaj()

    def bgt(self):
        return self.wjzxssaj()



