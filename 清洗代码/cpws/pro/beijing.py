from IKEA.mysql.mysqlbase import MysqlBase
from pyquery import PyQuery as pq
import re
import concurrent.futures




def beijing_article(items):
    d = pq(items['detail_response'])
    innerHTML = d('.article_con').text()
    innerHTML = re.sub('<!--\[if gte mso 9\]>.*<!\[endif\]-->', '',
                       innerHTML.replace('\\n', '').replace('document.getElementById("cc").innerHTML = unescape("',
                                                            '').replace('");', '')).encode('utf-8').decode(
        'unicode_escape')
    innerHTML = re.sub("spanstyle=.*?'>", '>', innerHTML)
    innerHTML = re.sub("style=.*?'>", '>', innerHTML)
    innerHTML = re.sub('<o:p></o:p>', '', innerHTML)
    innerHTML = re.sub('<span.*?>', '', innerHTML)
    innerHTML = re.sub('</span.*?>', '', innerHTML)
    innerHTML = re.sub('<html.*?>', '<html>', innerHTML)
    d = pq(innerHTML)
    innerHTML = d('p').text()
    innerHTML = re.sub('<>', '', innerHTML)
    innerHTML = re.sub('　　', '', innerHTML)
    innerHTML = re.sub('  ', '', innerHTML)
    innerHTML = re.sub('　', '', innerHTML)
    innerHTMLs = re.sub(' (\d+) ', '\\1', innerHTML).split(' ')
    return innerHTMLs

def beijing_list(items):
    d = pq(items['detail_response'])
    k = [i.text()[:-1] for i in d('.fd-lable').items()]
    j = [i.attr.value for i in d('.fd-input').items()]
    l = dict(zip(k, j))
    d = pq(items['list_response'])
    l['title'] = d('a').text()
    obj = {
        'type': l.get('案件类型')+'案件' if '案件' not in l.get('案件类型') else l.get('案件类型'),
        'title': l.get('title'),
        'case_no': l.get('案号'),
        'content_type': l.get('文书种类'),
        'court_name': l.get('审理法院'),
        'trial_date': re.sub('日', '', re.sub('月', '-', re.sub('年', '-', l.get('裁判日期')))),
        'reason': l.get('案由')
    }
    return obj



