from IKEA.mysql.mysqlbase import MysqlBase
import re
import json
from pyquery import PyQuery as pq


def guizhou_article(items):
    content = items['detail_response']
    content = json.loads(content)['data']
    content = content.replace('\\', '')
    content = re.sub(' style.*?>', '>', content)
    content = re.sub('　　', '', content)
    content = re.sub('　', '', content)
    content = '<HTML>' + content + '</html>'
    d = pq(content)
    dd = d('div')
    return dd.text().split(' ')

def guizhou_list(items):
    content = items['detail_response']
    content = json.loads(content)['data']
    content = content.replace('\\', '')
    content = re.sub(' style.*?>', '>', content)
    content = re.sub('　　', '', content)
    content = re.sub('　', '', content)
    content = '<HTML>' + content + '</html>'
    d = pq(content)
    dd = d('div')
    court = dd.text().split(' ')[0]
    case_no = dd.text().split(' ')[2]
    list_response = items['list_response']
    title = re.findall('title="(.*?)"', list_response)
    title = title[0] if title else ''
    obj = {
        'title': title,
        'court_name': court,
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
    for item in mb._execute("select * from judge_doc_guizhou limit 1;"):
        print('\n'.join(guizhou_article(item)))
        print(guizhou_list(item))