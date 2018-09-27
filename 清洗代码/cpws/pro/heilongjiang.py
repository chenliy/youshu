from IKEA.mysql.mysqlbase import MysqlBase
import re
from pyquery import PyQuery as pq
connector = {
    'host': '10.1.1.40',
    'user': 'xuewensi',
    'password': 'SE2LIPIhCo8gprAY',
    'db': 'judge_doc'
}

def heilongjiang_article(items):
    content = items['content']
    content = re.sub(' ', '', content)
    content = re.sub('　', '', content)
    content = re.sub('&nbsp;', '', content)
    d = pq(content)
    return d.text().split(' ')

def heilongjiang_list(items):
    obj = {
        'court_name': items.get('court'),
        'title': items.get('title')
    }
    return obj

