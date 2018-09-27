import os
import sys
sys.path.append(os.path.abspath(__file__ + "/../../../"))
from IKEA.mysql.mysqlbase import MysqlBase
from IKEA.cpws.pro.liaoning import liaoning_article
from IKEA.cpws.pro.liaoning import liaoning_list
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
connector = {
    'host': '10.1.1.40',
    'user': 'xuewensi',
    'password': 'SE2LIPIhCo8gprAY',
    'db': 'judge_doc'
}
def process_ws(items):
    l = liaoning_list(items)
    a = liaoning_article(items)
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
    items = {'is_process': '0', 'url': 'http://www.lnsfy.gov.cn:8080/susong51/cpws/paperView.htm?wsTypeSign=undefined&id=009d60b27cbeea03e41c2a41b9d950a6&fy=600', 'case_num': '', 'category': '', 'create_time': '2017-11-01 17:33:28', 'content': "<head><meta http-equiv='content-type' content='text/html;charset=UTF-8'></head><tr><td><div class='ws_title'>蔡恒涛故意伤害罪刑罚变更刑事裁定书</div></td></tr><tr><td><div class='ws_time'><span>发布日期：2017-10-31</span><input id='btn_print' value='打印阅览' class='btn' type='button'><input id='btn_download' value='文书下载' class='btn' type='button'></div></td></tr><tr><td><div class='hr1'></div></td></tr><tr><td><div class='print_area'><div class='doc_area'><h3 class='ws_con_hd'>辽宁省大连市中级人民法院</h3><h3 class='ws_con_hd'>刑事裁定书</h3><p class='ws_num'>（2017）辽02刑更392号</p><p class='ws_text'>罪犯蔡恒涛，男，1988年8月10日出生，汉族，辽宁省庄河市人，初中文化，现在辽宁省瓦房店监狱服刑。</p><p class='ws_text'>辽宁省大连市中级人民法院于2008年6月19日作出（2008）大刑一初字第101号刑事附带民事判决，以罪犯蔡恒涛犯故意伤害罪，判处无期徒刑，剥夺政治权利终身，连带赔偿附带民事诉讼原告人经济损失。判决发生法律效力后交付执行，2008年9月26日被投入辽宁省瓦房店监狱服刑。2011年2月21日经辽宁省高级人民法院以（2011）辽刑执字第171号刑事裁定，对其减为有期徒刑十九年，剥夺政治权利七年；2014年6月30日经本院以（2014）大审刑执字第838号刑事裁定，对其减去有期徒刑一年二个月，剥夺政治权利七年不变。现刑期至2028年12月20日止。</p><p class='ws_text'>执行机关辽宁省瓦房店监狱于2017年3月27日提出减刑建议，报送本院审理。本院依法予以公示并组成合议庭进行了审理。本案现已审理终结。</p><p class='ws_text'>执行机关减刑建议称：罪犯蔡恒涛在服刑期间，能认罪服法，接受改造，劳动积极，遵规守纪，确有悔改表现，向本院提出减刑建议。</p><p class='ws_text'>经审理查明，该犯入监服刑以来，能认罪悔罪；遵守法律法规及监规，服从管理，接受教育改造。现累计兑现记功奖励5次，表扬奖励2次。上述事实，有罪犯蔡恒涛的认罪悔过书、证人证言、改造表现材料、罪犯评审鉴定表、积分表奖表、奖励审批表等材料予以证实。</p><p class='ws_text'>本院认为，罪犯蔡恒涛服刑期间，确有悔改表现，符合减刑条件。依照《中华人民共和国刑法》第七十八条、第七十九条，《中华人民共和国刑事诉讼法》第二百六十二条第二款，《最高人民法院关于办理减刑、假释案件具体应用法律的规定》第二条之规定，裁定如下：</p><p class='ws_text'>对罪犯蔡恒涛减去有期徒刑八个月，剥夺政治权利七年不变。</p><p class='ws_text'>（刑期自2011年2月21日起至2028年4月20日止）</p><p class='ws_text'>本裁定送达后即发生法律效力。</p><p class='ws_descripttion'>审&nbsp;判&nbsp;长\u3000\u3000&nbsp;\u3000&nbsp;黄微</p><p class='ws_descripttion'>审&nbsp;判&nbsp;员\u3000\u3000&nbsp;&nbsp;夏红军</p><p class='ws_descripttion'>审&nbsp;判&nbsp;员\u3000\u3000&nbsp;&nbsp;李晓萃</p><p class='ws_descripttion'>二&Omicron;一七年四月二十五日</p><p class='ws_descripttion'>书&nbsp;记&nbsp;员\u3000\u3000&nbsp;&nbsp;刘丰采</p><p class='ws_descripttion'>&nbsp;</p></div></div></td></tr>", 'title': '蔡恒涛故意伤害罪刑罚变更刑事裁定书', 'court': '大连市中级人民法院', 'pub_date': '2017-10-31'}
    process_ws(items)
