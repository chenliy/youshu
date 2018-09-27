from pyquery import PyQuery as pq
from IKEA.mysql.mysqlbase import MysqlBase
from IKEA.cpws.config import reg
from IKEA.cpws.config import court_reg
from IKEA.cpws.wenshu.base import WenshuBase
from IKEA.cpws.qingxi import person_extract
from IKEA.cpws.qingxi import court_extract
from IKEA.cpws.qingxi import content_type_extract
from IKEA.cpws.qingxi import reason_extract
from IKEA.cpws.qingxi import local_person
from IKEA.cpws.qingxi import litigants_agent_extract
from IKEA.cpws.pro.shanghai import shanghai_aricle
import re
import json

# 测试环境
# crawl_connecter = {
#     'host': '10.1.1.30',
#     'user': 'root',
#     'password': 'root',
#     'db': 'test'
# }
#
# mb = MysqlBase(crawl_connecter)
# for items in mb._execute("select * from wenshu limit 11"):
#     d = pq(items['case_content'])
#     articles = re.sub('\u3000', '', re.sub('\n', '', d.text())).split(' ')
#     article = '\n'.join(articles)
#     ws = WenshuBase(article)
#
#
#     persons = person_extract('\n'.join(ws.role_paragraph))
#     for p in local_person(persons):
#         pass
#         # print(p)
#
#
#     litigants, agents = litigants_agent_extract('\n'.join(ws.role_paragraph))
#     for litigant in litigants:
#         print(json.dumps(litigants))
#     # print(agents)
#     # print('*'*100)
#
#     courts = court_extract('\n'.join(ws.court_paragraph))
#     for c in courts:
#         # print(c)
#         pass


connecter = {
    'host': '10.1.1.25',
    'user': 'crawler',
    'password': 'crawler',
    'db': 'judge_doc_shgy'
}

mb = MysqlBase(connecter)
for items in mb._execute("select * from judge_doc limit 10"):
    a = shanghai_aricle(items)
    litigants_agent_extract(a)