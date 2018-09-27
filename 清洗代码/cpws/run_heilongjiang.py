import os
import sys
sys.path.append(os.path.abspath(__file__ + "/../../../"))
from IKEA.mysql.mysqlbase import MysqlBase
from IKEA.cpws.pro.heilongjiang import heilongjiang_article
from IKEA.cpws.pro.heilongjiang import heilongjiang_list
from IKEA.cpws.wenshu.base import WenshuBase
from IKEA.cpws.qingxi import litigants_agent_extract
from IKEA.cpws.qingxi import court_extract
from IKEA.cpws.qingxi import reason_extract
from IKEA.cpws.qingxi import content_type_extract
from IKEA.cpws.qingxi import court_level_extract
from IKEA.cpws.qingxi import trial_date_extract
from IKEA.cpws.qingxi import trial_round_extract
from IKEA.cpws.qingxi import content_type_extract
from IKEA.cpws.qingxi import type_extract
from IKEA.cpws.qingxi import claim_extract
from IKEA.cpws.libs.process import process_bracket as pbracket
from IKEA.libs.date import update_time
from IKEA.libs.id import get_md5
from IKEA.es.postelastic import ines
from IKEA.es.postelastic import is_exists
# from IKEA.config import p_connecter as connector

connector = {
    'host': '10.1.1.40',
    'user': 'xuewensi',
    'password': 'SE2LIPIhCo8gprAY',
    'db': 'judge_doc'
}

def process_ws(items):
    l = heilongjiang_list(items)
    a = heilongjiang_article(items)

    ws = WenshuBase('\n'.join(a[5:]))
    litigants, agents = litigants_agent_extract('\n'.join(ws.role_paragraph))
    court_officers = court_extract('\n'.join(ws.court_paragraph))
    type = type_extract(l.get('title'))
    reasons = reason_extract(reason_description=ws.reason_description, title=l.get('title'), trial_type=type)
    trial_date = trial_date_extract(''.join(ws.court_paragraph))
    court_level = court_level_extract(l.get('court_name'))
    trial_round = trial_round_extract(l.get('title'))
    content_type = content_type_extract(ws.verdict_paragraph, l.get('title'))
    case_no = a[4]
    claim = ''
    if content_type == '判决书' and trial_round == '一审':
        for reason in reasons:
            if reason['reason_code_level2'] == 104 or reason['reason_code_level2'] == 105:
                claim = claim_extract(ws.claims_paragraphs)
    obj = {
        'case_no': pbracket(case_no),
        'reasons': reasons,
        'source': '黑龙江市高级人民法院',
        'type': type,
        'title': pbracket(l.get('title')),
        'content': '<br>'.join(a[5:]),
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
        'instrument_id': get_md5(l.get('title')) + get_md5(pbracket(case_no))
    }

    ines(id=obj['instrument_id'], path='http://10.1.1.28:9200/judge_doc/local_doc', data=obj)
    if is_exists(url='http://10.1.1.28:9200/judge_doc/total_doc', field='case_no', value=obj['case_no']):
        ines(id=obj['instrument_id'], path='http://10.1.1.28:9200/judge_doc/total_doc', data=obj)

if __name__ == '__main__':
    items = {'is_process': '0', 'url': 'http://www.susong51.com/cpws/paperView.htm?wsTypeSign=undefined&id=0b43a313a48d18efd58b968f47bbdbc9&fy=850', 'case_num': '', 'category': '', 'create_time': '2017-11-01 19:13:22', 'content': "<head><meta http-equiv='content-type' content='text/html;charset=UTF-8'></head><tr><td><div class='ws_title'>中国邮政储蓄银行股份有限公司嫩江县支行,高海龙信用卡纠纷一审裁定书</div></td></tr><tr><td><div class='ws_time'><span>发布日期：2017-10-31</span><input id='btn_print' value='打印阅览' class='btn' type='button'><input id='btn_download' value='文书下载' class='btn' type='button'></div></td></tr><tr><td><div class='hr1'></div></td></tr><tr><td><div class='print_area'><div class='doc_area'><h3 class='ws_con_hd'>黑龙江省嫩江县人民法院</h3><h3 class='ws_con_hd'>民事裁定书</h3><p class='ws_num'>（2017）黑1121民初2345号</p><p class='ws_text'>原告：中国邮政储蓄银行股份有限公司嫩江县支行，住所地黑龙江省黑河市嫩江县墨尔根大街400号。</p><p class='ws_text'>负责人：杨春华，职务行长。</p><p class='ws_text'>委托诉讼代理人：崔立娜，女，1978年1月11日出生，现住黑龙江省嫩江县。</p><p class='ws_text'>被告：高海龙，男，1980年3月7日出生，原住黑龙江省嫩江县，现下落不明。</p><p class='ws_text'>原告中国邮政储蓄银行股份有限公司嫩江县支行与被告高海龙信用卡纠纷一案，本院于2017年8月17日立案。原告于2017年10月30日以无法找到被告为由，向本院提出撤诉申请。</p><p class='ws_text'>本院认为，原告申请撤诉理由正当，符合有关法律规定。依照《中华人民共和国民事诉讼法》第一百四十五条第一款规定，裁定如下：</p><p class='ws_text'>准许原告中国邮政储蓄银行股份有限公司嫩江县支行撤诉。</p><p class='ws_text'>案件受理费50元，减半收取25元，由原告负担。</p><p class='ws_descripttion'>审判员\u3000\u3000杨艳红</p><p class='ws_descripttion'>二0一七年十月三十日</p><p class='ws_descripttion'>书记员\u3000\u3000崔雯雯</p></div></div></td></tr>", 'title': '中国邮政储蓄银行股份有限公司嫩江县支行,高海龙信用卡纠纷一审裁定书', 'court': '嫩江县人民法院', 'pub_date': '2017-10-31'}
    process_ws(items)