import os
import sys
sys.path.append(os.path.abspath(__file__ + "/../../../"))
from IKEA.mysql.mysqlbase import MysqlBase
from IKEA.cpws.pro.gansu import gansu_article
from IKEA.cpws.pro.gansu import gansu_list
from IKEA.cpws.wenshu.base import WenshuBase
from IKEA.cpws.qingxi import litigants_agent_extract
from IKEA.cpws.qingxi import court_extract
from IKEA.cpws.qingxi import reason_extract
from IKEA.cpws.qingxi import court_level_extract
from IKEA.cpws.qingxi import trial_date_extract
from IKEA.cpws.qingxi import trial_round_extract
from IKEA.cpws.qingxi import claim_extract
from IKEA.cpws.libs.process import process_bracket as pbracket
from IKEA.libs.date import update_time
from IKEA.libs.id import get_md5
from IKEA.es.postelastic import ines
from IKEA.es.postelastic import is_exists
from IKEA.config import p_connecter as connector
connecter = {
    'host': '10.1.1.40',
    'user': 'xuewensi',
    'password': 'SE2LIPIhCo8gprAY',
    'db': 'judge_doc'
}

def process_ws(items):
    l = gansu_list(items)
    a = gansu_article(items)
    ws = WenshuBase('\n'.join(a[5:]))
    litigants, agents = litigants_agent_extract('\n'.join(ws.role_paragraph))
    court_officers = court_extract('\n'.join(ws.court_paragraph))

    reasons = reason_extract(reason_description=ws.reason_description, title=l.get('title'), trial_type=l.get('type'))
    trial_date = trial_date_extract(''.join(ws.court_paragraph))
    court_level = court_level_extract(l.get('court_name'))
    trial_round = trial_round_extract(l.get('title'))
    claim = ''
    if l.get('content_type') == '判决书' and trial_round == '一审':
        for reason in reasons:
            if reason['reason_code_level2'] == 104 or reason['reason_code_level2'] == 105:
                claim = claim_extract(ws.claims_paragraphs)
    obj = {
        'case_no': pbracket(l.get('case_no')),
        'reasons': reasons,
        'source': '甘肃市高级人民法院',
        'type': l.get('type'),
        'title': pbracket(l.get('title')),
        'content': '<br>'.join(a[5:]),
        'agents': agents,
        'update_time': update_time(),
        'litigants': litigants,
        'content_type': l.get('content_type'),
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
    items = {'case_num': '（2017）甘2901执162号', 'pub_date': '2017-11-06', 'create_time': '2017-11-07 14:52:00', 'content': "<head><meta http-equiv='content-type' content='text/html;charset=UTF-8'></head><tr><td><div class='ws_title'>（2017）甘2901执162号.doc</div></td></tr><tr><td><div class='ws_time'><span>发布日期：2017-11-06</span><input id='btn_print' value='打印阅览' class='btn' type='button'><input id='btn_download' value='文书下载' class='btn' type='button'></div></td></tr><tr><td><div class='hr1'></div></td></tr><tr><td><div class='print_area'><div class='doc_area'><h3 class='ws_con_hd'>临夏市人民法院</h3><h3 class='ws_con_hd'>执行裁定书</h3><p class='ws_num'>（2017）甘2901执162号</p><p class='ws_text'>申请执行人胡加党，男，汉族，1974年11月28日出生，身份号码&times;&times;&times;，住临夏市。</p><p class='ws_text'>被执行人马军，男，回族，1982年2月4日出生，身份号码&times;&times;&times;，住临夏市。</p><p class='ws_text'>本院在执行申请执行人胡加党与被执行人马军装饰装修合同纠纷一案中，被执行人马军下落不明，经通过四查，也无可供执行的财产。依据《最高人民法院关于适用&lt;中华人民共和国民事诉讼法&gt;的解释》第五百一十九条的规定，裁定如下：</p><p class='ws_text'>终结本次执行程序。</p><p class='ws_text'>申请执行人发现被执行人有可供执行财产的，可以再次申请执行全部债权。</p><p class='ws_text'>本裁定送达后即发生法律效力。</p><p class='ws_text'>审&nbsp; 判&nbsp; 员&nbsp;&nbsp; 康海龙</p><p class='ws_descripttion'>二〇一七年九月十六日</p><p class='ws_text'>书&nbsp; 记&nbsp; 员&nbsp;&nbsp; 吴楠</p><p class='ws_text'>&nbsp;</p></div></div></td></tr>", 'url': 'http://61.178.55.5:7080/susong51/cpws/paperView.htm?wsTypeSign=undefined&id=135709b29fcbd34e492e1a5cbbbc3056&fy=3750', 'category': '执行裁定书', 'is_process': '0', 'title': '（2017）甘2901执162号.doc', 'court': '临夏市人民法院'}
    process_ws(items)