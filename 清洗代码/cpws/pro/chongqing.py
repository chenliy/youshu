from IKEA.mysql.mysqlbase import MysqlBase
import re
from pyquery import PyQuery as pq

connecter = {
    'host': '10.1.1.40',
    'user': 'xuewensi',
    'password': 'SE2LIPIhCo8gprAY',
    'db': 'judge_doc'
}
def chongqing_article(items):
    content = items['content']
    content = re.sub('  ', '', content)
    content = re.sub('　　', '', content)
    d = pq(content)
    dd = d('span')
    return dd.text().split(' ')

def chongqing_list(items):
    content = items['content']
    content = re.sub('  ', '', content)
    content = re.sub('　　', '', content)
    d = pq(content)
    dd = d('span')
    case_no = dd.text().split(' ')[4]

    obj = {
        'type': items.get('category'),
        'title': items.get('title'),
        'court_name': items.get('court'),
        'case_no': case_no
    }
    return obj



if __name__ == '__main__':
    mb = MysqlBase(connecter)
    for item in mb._execute("select * from judge_doc_chongqing limit 1;"):
        print(chongqing_list(item))