import os
import sys
sys.path.append(os.path.abspath(__file__ + "/../../../"))
from IKEA.mysql.mysqlbase import MysqlBase
from IKEA.cpws.pro.jilin import jilin_article
from IKEA.cpws.pro.jilin import jilin_list
from IKEA.cpws.wenshu.base import WenshuBase
from IKEA.cpws.qingxi import litigants_agent_extract
from IKEA.cpws.qingxi import court_extract
from IKEA.cpws.qingxi import reason_extract
from IKEA.cpws.qingxi import court_level_extract
from IKEA.cpws.qingxi import trial_date_extract
from IKEA.cpws.qingxi import trial_round_extract
from IKEA.cpws.qingxi import claim_extract
from IKEA.cpws.qingxi import content_type_extract
from IKEA.cpws.qingxi import type_extract
from IKEA.cpws.libs.process import process_bracket as pbracket
from IKEA.libs.date import update_time
from IKEA.libs.id import get_md5
from IKEA.es.postelastic import ines
from IKEA.es.postelastic import is_exists
from IKEA.config import p_connecter as connector

def process_ws(items):
    l = jilin_list(items)
    a = jilin_article(items)
    ws = WenshuBase('\n'.join(a[3:]))
    litigants, agents = litigants_agent_extract('\n'.join(ws.role_paragraph))
    court_officers = court_extract('\n'.join(ws.court_paragraph))
    type = type_extract(l.get('title'))
    reasons = reason_extract(reason_description=ws.reason_description, title=l.get('title'), trial_type=type)
    trial_date = trial_date_extract(''.join(ws.court_paragraph))
    court_level = court_level_extract(l.get('court_name'))
    trial_round = trial_round_extract(l.get('title'))
    content_type = content_type_extract(ws.verdict_paragraph, l.get('title'))
    case_no = l.get('case_no')
    claim = ''
    if content_type == '判决书' and trial_round == '一审':
        for reason in reasons:
            if reason['reason_code_level2'] == 104 or reason['reason_code_level2'] == 105:
                claim = claim_extract(ws.claims_paragraphs)
    obj = {
        'case_no': pbracket(l.get('case_no')),
        'reasons': reasons,
        'source': '辽宁高级人民法院',
        'type': type,
        'title': pbracket(l.get('title')),
        'content': '<br>'.join(a),
        'agents': agents,
        'update_time': update_time(),
        'litigants': litigants,
        'content_type': content_type,
        'trial_round': trial_round,
        'court_level': court_level,
        'verdict': ws.verdict,
        'trial_date': trial_date,
        'court_officers': court_officers,
        'court_name': l.get('court_name'),
        'claim': claim,
        'operator': 'leifeng',
        'instrument_id': get_md5(l.get('title')) + get_md5(pbracket(l.get('case_no')))
    }

    ines(id=obj['instrument_id'], path='http://10.1.1.28:9200/judge_doc/local_doc', data=obj)
    if is_exists(url='http://10.1.1.28:9200/judge_doc/total_doc', field='case_no', value=obj['case_no']):
        ines(id=obj['instrument_id'], path='http://10.1.1.28:9200/judge_doc/total_doc', data=obj)


if __name__ == '__main__':

    connector = {
        'host': '10.1.1.40',
        'user': 'xuewensi',
        'password': 'SE2LIPIhCo8gprAY',
        'db': 'judge_doc'
    }



    mb = MysqlBase(connector)
    for i in range(1):
        for items in mb._execute("select * from judge_doc_jilin  limit 1".format()):

            print(items['id'])
            try:
                l = jilin_list(items)
                a = jilin_article(items)
                ws = WenshuBase('\n'.join(a[3:]))
                litigants, agents = litigants_agent_extract('\n'.join(ws.role_paragraph))
                court_officers = court_extract('\n'.join(ws.court_paragraph))
                type = type_extract(l.get('title'))
                reasons = reason_extract(reason_description=ws.reason_description, title=l.get('title'), trial_type=type)
                trial_date = trial_date_extract(''.join(ws.court_paragraph))
                court_level = court_level_extract(l.get('court_name'))
                trial_round = trial_round_extract(l.get('title'))
                content_type = content_type_extract(ws.verdict_paragraph, l.get('title'))
                case_no = l.get('case_no')
                claim = ''
                if content_type == '判决书' and trial_round == '一审':
                    for reason in reasons:
                        if reason['reason_code_level2'] == 104 or reason['reason_code_level2'] == 105:
                            claim = claim_extract(ws.claims_paragraphs)
                obj = {
                    'case_no': pbracket(l.get('case_no')),
                    'reasons': reasons,
                    'source': '吉林高级人民法院',
                    'type': type,
                    'title': pbracket(l.get('title')),
                    'content': '<br>'.join(a),
                    'agents': agents,
                    'update_time': update_time(),
                    'litigants': litigants,
                    'content_type': content_type,
                    'trial_round': trial_round,
                    'court_level': court_level,
                    'verdict': ws.verdict,
                    'trial_date': trial_date,
                    'court_officers': court_officers,
                    'court_name': l.get('court_name'),
                    'claim': claim,
                    'operator': 'leifeng',
                    'instrument_id': get_md5(l.get('title')) + get_md5(pbracket(l.get('case_no')))
                }

                ines(id=obj['instrument_id'], path='http://10.1.1.28:9200/judge_doc/local_doc', data=obj)
                if is_exists(url='http://10.1.1.28:9200/judge_doc/total_doc', field='case_no', value=obj['case_no']):
                    ines(id=obj['instrument_id'], path='http://10.1.1.28:9200/judge_doc/total_doc', data=obj)
            except e:
                print(e)