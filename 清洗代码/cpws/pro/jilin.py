from IKEA.mysql.mysqlbase import MysqlBase
import re
from pyquery import PyQuery as pq


def jilin_article(items):
    content = items['content']
    content = re.sub('　　', '', content)
    content = re.sub('  ', '', content)
    content = re.sub('　', '', content)
    d = pq(content)
    dd = d('p')
    return dd.text().split(' ')

def jilin_list(items):
    content = items['content']
    content = re.sub('  ', '', content)
    content = re.sub('　　', '', content)
    d = pq(content)
    dd = d('p')
    case_no = dd.text().split(' ')[0]

    obj = {
        'title': items.get('title'),
        'court_name': items.get('court'),
        'case_no': case_no
    }
    return obj


connecter = {
    'host': '10.1.1.40',
    'user': 'xuewensi',
    'password': 'SE2LIPIhCo8gprAY',
    'db': 'judge_doc'
}


if __name__ == '__main__':
    mb = MysqlBase(connecter)
    for item in mb._execute("select * from judge_doc_jilin limit 1;"):
        print('\n'.join(jilin_article(item)))
        print(jilin_list(item))