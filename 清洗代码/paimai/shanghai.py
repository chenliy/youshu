from IKEA.config import judge_connecter as connecter
from IKEA.mysql.mysqlbase import MysqlBase
from pyquery import PyQuery as pq
import re

mb = MysqlBase(connecter)
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



for items in mb._execute("SELECT * FROM judge_doc_shgy.pinggupaimai limit 1000; "):
    try:
        obj = {}
        d = pq(items['content'])
        key_msg = [each.text() for n, each in enumerate(d(".tdnr").items()) if n % 2 == 0]
        value_msg = [each.text() for n, each in enumerate(d(".tdnr").items()) if n % 2 != 0]
        msg = dict(zip(key_msg, value_msg))
        limiting_cause = [d.text() for d in d('.nr div.nr').items() if len(d.text()) > 10][0]
        court_name, tel_of_court = msg['承办法院、联系电话'].split('\xa0\xa0')
        auction_house, tel_of_auction = msg['拍卖机构'].split(':')
        name, business_entity = extract_business_entity(msg['被执行人'])
        obj = {
            'exposure_type': '执行案件评估拍卖',
            'identity': '被执行人',
            'name': name,
            'business_entity': business_entity,
            'address': msg['被执行人地址'],
            'execute_money': msg['执行标的金额（元）'],
            'limiting_cause': limiting_cause,
            'case_code': msg['案号'],
            'court_name': court_name,
            'source': '上海市高级人民法院',
            'tel_of_court': tel_of_court,
            'execution_applicant': msg['申请执行人'],
            'auction_house': auction_house,
            'tel_of_auction': tel_of_auction
        }
        mb.into_file('paimai', *obj.keys(), **obj)
    except:
        pass