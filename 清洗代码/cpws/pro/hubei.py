from IKEA.mysql.mysqlbase import MysqlBase
import re
from pyquery import PyQuery as pq

connecter = {
    'host': '10.1.1.40',
    'user': 'xuewensi',
    'password': 'SE2LIPIhCo8gprAY',
    'db': 'judge_doc'
}
def hubei_article(items):
    content = items['content']
    content = re.sub('&lt;', '<', content)
    content = re.sub('&gt;', '>', content)
    content = re.sub('style=.*?>', '>', content)
    content = re.sub(' >', '>', content)
    content = re.sub('　　', '', content)
    content = content[content.find('<BODY>'):]
    content = re.sub('<BODY>;', '', content)
    content = re.sub(' ', '', content)
    content = re.sub('\u3000', '', content)
    d = pq('<HTML>' + content)
    dd = d('div')
    return dd.text().split(' ')

def hubei_list(items):
    content = items['content']
    title = content[2:content.find('.htm";')]
    content = re.sub('&lt;', '<', content)
    content = re.sub('&gt;', '>', content)
    content = re.sub('style=.*?>', '>', content)
    content = re.sub(' >', '>', content)
    content = re.sub('　　', '', content)
    content = content[content.find('<BODY>'):]
    content = re.sub('<BODY>;', '', content)
    content = re.sub(' ', '', content)
    content = re.sub('\u3000', '', content)
    d = pq('<HTML>' + content)
    dd = d('div')
    case_no = dd.text().split(' ')[2]
    court = dd.text().split(' ')[0]
    obj = {
        'type': re.sub('文书', '案件', items.get('category')),
        'title': title,
        'court_name': court,
        'case_no': case_no
    }
    return obj



if __name__ == '__main__':
    mb = MysqlBase(connecter)
    for item in mb._execute("select * from judge_doc_hubei where id = 5;"):

        print('\n'.join(hubei_article(item)))