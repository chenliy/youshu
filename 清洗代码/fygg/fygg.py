import os
import sys
sys.path.append(os.path.abspath(__file__ + "/../../../"))

from pyquery import PyQuery as pq
from IKEA.libs.id import get_md5
from IKEA.es.postelastic import ines
import re
from datetime import date
from IKEA.config import p_connecter as connecter
from IKEA.mysql.mysqlbase import  MysqlBase

def extract_fygg(article):
    d = pq(article)
    title = d('.wby')
    title('font').remove()
    ann_type, defendant = title.text().strip().split('——')
    content = d('.nrtxt')
    content('p').remove()
    announcer, ann_date = content('span').text().split(' ')
    content('span').remove()
    c = content.text()
    i = c.find('：')
    defendant_origin = c[:i]
    defendants = c[:i].strip().split('、')
    defendants.append(defendant)
    ann_content = c[i + 1:].strip()
    dd = re.findall('(\d+)年(\d+)月(\d+)日', ann_date)[0]

    for d in defendants:
        yield {
            'ann_type': ann_type,
            'announcer': announcer,
            'defendant': d,
            'defendant_origin': defendant_origin,
            'ann_date': date(year=int(dd[0]), month=int(dd[1]), day=int(dd[2])).isoformat(),
            'ann_content': ann_content,
            'ann_html': article
        }



mb = MysqlBase(connecter)
for item in mb._execute("select * from sh_sdgg where is_process = 0"):
    article = items['detail']
    for e in extract_fygg(article):
        id = get_md5(e['ann_type']) + get_md5(e['defendant']) + get_md5(e['ann_date'])
        e['id'] = id
        ines(id=id, path='http://10.1.1.28:9200/court_announcement/court_announcement', data=e)