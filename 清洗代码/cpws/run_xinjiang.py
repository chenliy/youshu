import os
import sys
sys.path.append(os.path.abspath(__file__ + "/../../../"))
from IKEA.mysql.mysqlbase import MysqlBase
from IKEA.cpws.pro.xinjiang import xinjiang_article
from IKEA.cpws.pro.xinjiang import xinjiang_list
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
    l = xinjiang_list(items)
    a = xinjiang_article(items)
    ws = WenshuBase('\n'.join(a[1:]))
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
        'source': '新疆高级人民法院',
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
    items = {'is_process': '0', 'court': '鄯善县人民法院', 'title': 'دەۋاگەر ئابدۇۋەل ئوسماننىڭ جاۋاپكار شەمشىدىن ئەيسا ئۈستىدىن ئەرز قىل', 'case_num': '', 'create_time': '2017-11-01 15:52:34', 'category': '', 'content': '<head><meta http-equiv=\'content-type\' content=\'text/html;charset=UTF-8\'></head><tr><td><div class=\'ws_title\'>دەۋاگەر ئابدۇۋەل ئوسماننىڭ جاۋاپكار شەمشىدىن ئەيسا ئۈستىدىن ئەرز قىلغان ئىلىم- بېرىم ماجرا دىلوسى</div></td></tr><tr><td><div class=\'ws_time\'><span>ئېلان قىلغان كۈن：2017-10-30</span><input id=\'btn_print\' value=\'بېسىش\' class=\'btn\' type=\'button\'><input id=\'btn_download\' value=\'چۈشۈرۈش\' class=\'btn\' type=\'button\'></div></td></tr><tr><td><div class=\'hr1\'></div></td></tr><tr><td><div class=\'print_area\'><div class=\'doc_area\'><p><img src="../store/cpws/writ/20171030/2ab800b113bb10d8318b26020439d1df/000.png"/></p><p><img src="../store/cpws/writ/20171030/2ab800b113bb10d8318b26020439d1df/001.png"/></p></div></div></td></tr>', 'pub_date': '2017-10-30', 'url': 'http://220.171.35.30:8080/susong51/cpws/paperView.htm?wsTypeSign=undefined&id=2ab800b113bb10d8318b26020439d1df&fy=4050'}
    process_ws(items)
    #
    # connector = {
    #     'host': '10.1.1.40',
    #     'user': 'xuewensi',
    #     'password': 'SE2LIPIhCo8gprAY',
    #     'db': 'judge_doc'
    # }
    #
    # mb = MysqlBase(connector)
    # for i in range(1):
    #     for items in mb._execute("select * from judge_doc_xinjiang  limit 1".format()):
    #
    #         print(items['id'])
    #         try:
    #             l = xinjiang_list(items)
    #             a = xinjiang_article(items)
    #             ws = WenshuBase('\n'.join(a[3:]))
    #             litigants, agents = litigants_agent_extract('\n'.join(ws.role_paragraph))
    #             court_officers = court_extract('\n'.join(ws.court_paragraph))
    #             type = type_extract(l.get('title'))
    #             reasons = reason_extract(reason_description=ws.reason_description, title=l.get('title'), trial_type=type)
    #             trial_date = trial_date_extract(''.join(ws.court_paragraph))
    #             court_level = court_level_extract(l.get('court_name'))
    #             trial_round = trial_round_extract(l.get('title'))
    #             content_type = content_type_extract(ws.verdict_paragraph, l.get('title'))
    #             case_no = l.get('case_no')
    #             claim = ''
    #             if content_type == '判决书' and trial_round == '一审':
    #                 for reason in reasons:
    #                     if reason['reason_code_level2'] == 104 or reason['reason_code_level2'] == 105:
    #                         claim = claim_extract(ws.claims_paragraphs)
    #             obj = {
    #                 'case_no': pbracket(l.get('case_no')),
    #                 'reasons': reasons,
    #                 'source': '新疆高级人民法院',
    #                 'type': type,
    #                 'title': pbracket(l.get('title')),
    #                 'content': '<br>'.join(a),
    #                 'agents': agents,
    #                 'update_time': update_time(),
    #                 'litigants': litigants,
    #                 'content_type': content_type,
    #                 'trial_round': trial_round,
    #                 'court_level': court_level,
    #                 'verdict': ws.verdict,
    #                 'trial_date': trial_date,
    #                 'court_officers': court_officers,
    #                 'court_name': l.get('court_name'),
    #                 'claim': claim,
    #                 'operator': 'leifeng',
    #                 'instrument_id': get_md5(l.get('title')) + get_md5(pbracket(l.get('case_no')))
    #             }
    #
    #             ines(id=obj['instrument_id'], path='http://10.1.1.28:9200/judge_doc/local_doc', data=obj)
    #             if is_exists(url='http://10.1.1.28:9200/judge_doc/total_doc', field='case_no', value=obj['case_no']):
    #                 ines(id=obj['instrument_id'], path='http://10.1.1.28:9200/judge_doc/total_doc', data=obj)
    #         except:
    #             print('error')