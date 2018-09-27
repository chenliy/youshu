from IKEA.mysql.mysqlbase import MysqlBase
from pyquery import PyQuery as pq
import re
import json
import concurrent.futures


connecter = {
    'host': '10.1.1.30',
    'user': 'root',
    'password': 'root',
    'db': 'test'
}

def zhejiang_article(items):
    detail_response = items['detail_response']
    html = re.findall('(<html.*?</html>)', detail_response)[0]
    html = re.sub('style.*?>', '>', html)
    html = re.sub('<html.*?>', '<html>', html)
    html = re.sub('<meta.*?>', '', html)
    html = re.sub(' >', '>', html)
    html = re.sub('</p><p>', '', html)
    html = re.sub('&#xa0;', '', html)
    html = re.sub('　　　', '', html)
    d = pq(html)
    return d('span').text().split(' ')

def zhejiang_list(items):
    l = items['list_response']
    l = eval(l)
    obj = {
        'type': l.setdefault('AJLB'),
        'court_name': l.setdefault('CourtName'),
        'case_no': l.setdefault('AH')
    }
    return obj

mb = MysqlBase(connecter)
for items in mb._execute("select * from wenshu_zhejiang1 limit 1"):
    print(zhejiang_list(items))
    print(zhejiang_article(items))