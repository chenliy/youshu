from IKEA.mysql.mysqlbase import MysqlBase
import re
from pyquery import PyQuery as pq


def fujian_article(items):
    content = items['content']
    content = re.sub(' style=.*?>', '>', content)
    content = content.replace('</div>&#13;', '')
    content = content[content.find('<title/>')+8:]
    content = re.sub(' ', '', content)
    content = re.sub('　', '', content)
    content = re.sub('　　', '', content)
    content = '<html>{}</html>'.format(content)
    d = pq(content)
    dd = d('div')
    return dd.text().split(' ')

def fujian_list(items):
    content = items['content']
    content = re.sub(' style=.*?>', '>', content)
    content = content.replace('</div>&#13;', '')
    content = content[content.find('<title/>') + 8:]
    content = re.sub('　　', '', content)
    content = re.sub('　', '', content)
    content = re.sub(' ', '', content)
    content = '<html>{}</html>'.format(content)
    d = pq(content)
    dd = d('div')
    case_no = dd.text().split(' ')[2]
    print(items.get('category'))
    obj = {
        'type': items.get('category'),
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
    for item in mb._execute("select * from judge_doc_fujian limit 1;"):
        print('\n'.join(fujian_article(item)))
        print(fujian_list(item))