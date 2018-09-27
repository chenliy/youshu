from IKEA.mysql.mysqlbase import MysqlBase
from pyquery import PyQuery as pq
import re


def gansu_article(items):
    content = items['content']
    content = re.sub(' ', '', content)
    content = re.sub('　', '', content)
    content = re.sub('&nbsp;', '', content)
    d = pq(content)
    return d.text().split(' ')

def gansu_list(items):
    category = ''.join([k for k in items.get('category') if k.isalpha()])
    content_type = category[-3:] if '书' in category[-3:] else ''
    if '刑事' in category[:-3]:
        type = '刑事案件'
    elif '民事' in category[:-3] and '刑事' not in category[:-3]:
        type = '民事案件'
    elif '行政' in category[:-3] and '赔偿' not in category[:-3]:
        type = '行政案件'
    elif '赔偿' in category[:-3]:
        type = '赔偿案件'
    elif '执行' in category[:-3]:
        type = '执行案件'
    else:
        type = ''

    obj = {
        'type': type,
        'title': items.get('title'),
        'case_no': items.get('case_num'),
        'content_type': content_type,
        'court_name': items.get('court')
    }
    return obj

