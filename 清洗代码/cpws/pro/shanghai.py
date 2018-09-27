from IKEA.mysql.mysqlbase import MysqlBase
from IKEA.cpws.qingxi import litigants_agent_extract
from pyquery import PyQuery as pq
import re


# def shanghai_aricle(items):
#     d = pq(re.sub('<?xml.*?/>', '', items['content']))
#     flag = 10000
#     content = re.sub('， ', '', re.sub(' 年 ', '年', re.sub(' 月 ', '月', re.sub(' 日 ', '日', d('p').text()))))
#     court = ''
#     for n, tr in enumerate(d('tr').items()):
#         if tr('.nrtxt'):
#             flag = n
#         if n > flag:
#             court = court + re.sub('\xa0\xa0', '', tr.text()) + '\n'
#     return '\n'.join(content.split(' ') + court.split('\n')[:-1])

# def shanghai_content(items):
#     d = pq(re.sub('<?xml.*?/>', '', items['content']))
#     flag = 10000
#     content = re.sub('。', '。 ', re.sub(' ', '', d('p').text()))
#     court = ''
#     for n, tr in enumerate(d('tr').items()):
#         if tr('.nrtxt'):
#             flag = n
#         if n > flag:
#             court = court + re.sub('\xa0\xa0', '', tr.text()) + '\n'
#     return '\n'.join(content.split(' ') + court.split('\n')[:-1])

def shanghai_aricle(items):
    article = items['content']
    article = re.sub(' style.*?>', '>', article)
    article = re.sub('<?xml.*?/>', '', article)
    article = re.sub('<span.*?>', '', article)
    article = re.sub('</span.*?>', '', article)
    d = pq(article)
    content = d('p').text()
    court = ''
    flag = 10000
    for n, tr in enumerate(d('tr').items()):
        if tr('.nrtxt'):
            flag = n
        if n > flag:
            court = court + re.sub('\xa0\xa0', '', tr.text()) + '\n'
    return '\n'.join(content.split(' ') + court.split('\n')[:-1])

def shanghai_list(items):
    return {
        'case_no': items['case_num'].strip(),
        'title': items['title'].strip(),
        'trial_round': items['level'].strip(),
        'trial_date': items['close_date'].strip(),
        'type': items['category'].strip()
    }

def shanghai_court_name(items):
    d = pq(items['content'])
    return d('.style2').text()

def shanghai_trial_type(items):
    apartment = items['apartment']
    title = items['title']
    if '行政' in apartment:
        return '行政案件'
    elif '刑' in apartment:
        return '刑事案件'
    elif '执行' in apartment:
        return '执行案件'
    elif '审监庭' in apartment and ('民事' not in title and '刑事' not in title and '行政' not in title):
        return ''
    else:
        return '民事案件'

