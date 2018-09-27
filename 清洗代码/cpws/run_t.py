import os
import sys
sys.path.append(os.path.abspath(__file__ + "/../../../"))
from IKEA.mysql.mysqlbase import MysqlBase
from IKEA.cpws.pro.shanghai import shanghai_aricle
from IKEA.cpws.pro.shanghai import shanghai_list
from IKEA.cpws.pro.shanghai import shanghai_court_name
from IKEA.cpws.pro.shanghai import shanghai_trial_type
from IKEA.cpws.qingxi import litigants_agent_extract
from IKEA.cpws.qingxi import court_extract
from IKEA.cpws.qingxi import content_type_extract
from IKEA.cpws.qingxi import reason_extract
from IKEA.cpws.qingxi import court_level_extract
from IKEA.cpws.qingxi import claim_extract
from IKEA.cpws.wenshu.base import WenshuBase
from IKEA.cpws.libs.process import process_bracket as pbracket
from IKEA.libs.id import get_md5
from IKEA.libs.date import update_time
from IKEA.es.postelastic import ines
from IKEA.es.postelastic import is_exists
from IKEA.config import shanghai_connecter as connecter
import json
import re



def process_ws(items):
    obj = {}
    shls = shanghai_list(items)
    trial_type = shanghai_trial_type(items)
    court_name = shanghai_court_name(items)
    # content = shanghai_content(items)
    article = shanghai_aricle(items)

    ws = WenshuBase(article)
    litigants, agents = litigants_agent_extract('\n'.join(ws.role_paragraph))
    court_officers = court_extract('\n'.join(ws.court_paragraph))
    content_type = content_type_extract(ws.verdict_paragraph, shls['title'])
    reasons = reason_extract(reason_description=ws.reason_description, title=shls['title'], trial_type=trial_type)
    court_level = court_level_extract(court_name)
    claim = ''
    if content_type == '判决书' and shls['trial_round'] == '一审':
        for reason in reasons:
            if reason['reason_code_level2'] == 104 or reason['reason_code_level2'] == 105:
                claim = claim_extract(ws.claims_paragraphs)
    obj = {
        'case_no': pbracket(shls['case_no']),
        'reasons': reasons,
        'source': '上海市高级人民法院',
        'type': trial_type,
        'title': pbracket(shls['title']),
        'content': re.sub('\n', '<br>', article),
        'agents': agents,
        'update_time': update_time(),
        'litigants': litigants,
        'content_type': content_type,
        'trial_round': shls['trial_round'],
        'court_level': court_level,
        'verdict': ws.verdict,
        'trial_date': shls['trial_date'],
        'court_officers': court_officers,
        'court_name': court_name,
        'claim': claim,
        'operator': 'leifeng',
        'instrument_id': get_md5(shls['title']) + get_md5(pbracket(shls['case_no']))
    }
    ines(id=obj['instrument_id'], path='http://10.1.1.28:9200/judge_doc/local_doc', data=obj)
    if is_exists(url='http://10.1.1.28:9200/judge_doc/total_doc', field='case_no', value=obj['case_no']):
        ines(id=obj['instrument_id'], path='http://10.1.1.28:9200/judge_doc/total_doc', data=obj)

if __name__ == '__main__':
    id = 1
    l_id = 1
    r_id = 1
    mb = MysqlBase(connecter)
    for i in range(1):
        for items in mb._execute(
                "select * from `judge_doc_new` where id = '85737' ".format((i+3) * 1000)):
            print('process id:{}'.format(items['id']))
            print(items)
            # obj = {}
            # id = id + 1
            # table_id = items['id']
            # shls = shanghai_list(items)
            # trial_type = shanghai_trial_type(items)
            # court_name = shanghai_court_name(items)
            # # content = shanghai_content(items)
            # article = shanghai_aricle(items)
            #
            # ws = WenshuBase(article)
            # litigants, agents = litigants_agent_extract('\n'.join(ws.role_paragraph))
            # court_officers = court_extract('\n'.join(ws.court_paragraph))
            # content_type = content_type_extract(ws.verdict_paragraph, shls['title'])
            # reasons = reason_extract(reason_description=ws.reason_description, title=shls['title'], trial_type=trial_type)
            # court_level = court_level_extract(court_name)
            # claim = ''
            # if content_type == '判决书' and shls['trial_round'] == '一审':
            #     for reason in reasons:
            #         if reason['reason_code_level2'] == 104 or reason['reason_code_level2'] == 105:
            #             claim = claim_extract(ws.claims_paragraphs)
            # obj = {
            #     'case_no': pbracket(shls['case_no']),
            #     'reasons': reasons,
            #     'source': '上海市高级人民法院',
            #     'type': trial_type,
            #     'title': pbracket(shls['title']),
            #     'content': re.sub('\n', '<br>', article),
            #     'agents': agents,
            #     'update_time': update_time(),
            #     'litigants': litigants,
            #     'content_type': content_type,
            #     'trial_round': shls['trial_round'],
            #     'court_level': court_level,
            #     'verdict': ws.verdict,
            #     'trial_date': shls['trial_date'],
            #     'court_officers': court_officers,
            #     'court_name': court_name,
            #     'claim': claim,
            #     'operator': 'leifeng',
            #     'instrument_id': get_md5(shls['title']) + get_md5(pbracket(shls['case_no']))
            # }
            # ines(id=obj['instrument_id'], path='http://10.1.1.28:9200/judge_doc/local_doc', data=obj)
            # if is_exists(url='http://10.1.1.28:9200/judge_doc/total_doc', field='case_no', value=obj['case_no']):
            #     ines(id=obj['instrument_id'], path='http://10.1.1.28:9200/judge_doc/total_doc', data=obj)
















