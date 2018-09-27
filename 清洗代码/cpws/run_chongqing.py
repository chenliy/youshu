import os
import sys
sys.path.append(os.path.abspath(__file__ + "/../../../"))
from IKEA.mysql.mysqlbase import MysqlBase
from IKEA.cpws.pro.chongqing import chongqing_article
from IKEA.cpws.pro.chongqing import chongqing_list
from IKEA.cpws.wenshu.base import WenshuBase
from IKEA.cpws.qingxi import litigants_agent_extract
from IKEA.cpws.qingxi import court_extract
from IKEA.cpws.qingxi import reason_extract
from IKEA.cpws.qingxi import content_type_extract
from IKEA.cpws.qingxi import court_level_extract
from IKEA.cpws.qingxi import trial_date_extract
from IKEA.cpws.qingxi import trial_round_extract
from IKEA.cpws.qingxi import type_extract
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
    l = chongqing_list(items)
    a = chongqing_article(items)

    ws = WenshuBase('\n'.join(a[4:]))
    litigants, agents = litigants_agent_extract('\n'.join(ws.role_paragraph))
    court_officers = court_extract('\n'.join(ws.court_paragraph))
    type = l.get('type')
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
        'case_no': pbracket(case_no),
        'reasons': reasons,
        'source': '重庆市高级人民法院',
        'type': type,
        'title': pbracket(l.get('title')),
        'content': '<br>'.join(ws.articles),
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
        'operator': 'leifeng',
        'instrument_id': get_md5(l.get('title')) + get_md5(pbracket(case_no)),
        'claim': claim
    }
    ines(id=obj['instrument_id'], path='http://10.1.1.28:9200/judge_doc/local_doc', data=obj)
    if is_exists(url='http://10.1.1.28:9200/judge_doc/total_doc', field='case_no', value=obj['case_no']):
        ines(id=obj['instrument_id'], path='http://10.1.1.28:9200/judge_doc/total_doc', data=obj)


if __name__ == '__main__':
    items = {'is_process': '0', 'url': 'http://www.cqfygzfw.com/court/cpws/cpwsView.jsp?jlid=M52cf8ffedf-8174-49a6-af85-16bf68673ee7&ajlx=1', 'case_num': '', 'category': '刑事案件', 'create_time': '2017-11-01 19:02:40', 'content': '<div class="r_view">\n<h1>杜成国妨害公务罪一审刑事判决书</h1>\n<h2>\n           <div>\n                   <form action="http://www.cqfygzfw.com/court/cpwsAction_download.shtml" method="post" name="addNewsForm" id="addNewsForm" theme="simple" enctype="multipart/form-data">\n                   <div id="wsTime" align="center">\n                \t <input type="hidden" id="jlid" name="wssw.jlid" value="M52cf8ffedf-8174-49a6-af85-16bf68673ee7" />\n                \t </div>\n                  <div id="wsTime" align="center"><span>提交时间：2017-11-01 00:00:00 </span>\n                \n                  <a href="http://www.cqfygzfw.com/court/cpws/cpwsView.jsp?jlid=M52cf8ffedf-8174-49a6-af85-16bf68673ee7&amp;ajlx=1" onclick="serachClick();" class="s_1">下载文书</a></div>\n                  \n                   </form>\n                 \n                 \n                  </div>\n</h2>\n             \n           <div id="DocArea" style="line-height:32px; font-size:18px;">\n\n<meta http-equiv="Content-Type" content="text/html; charset=GB2312" />\n<style type="text/css">.b1{white-space-collapsing:preserve;}\n.b2{margin: 1.4569445in 1.0236111in 1.3784722in 1.0236111in;}\n.s1{font-weight:bold;color:black;}\n.s2{color:black;}\n.p1{margin-right:0.0875in;text-align:center;hyphenate:auto;font-family:宋体;font-size:22pt;}\n.p2{margin-left:6.9444446E-4in;text-align:center;hyphenate:auto;font-family:宋体;font-size:26pt;}\n.p3{text-indent:0.44444445in;text-align:right;hyphenate:auto;font-family:仿宋;font-size:16pt;}\n.p4{text-indent:0.44444445in;text-align:justify;hyphenate:auto;font-family:仿宋;font-size:16pt;}\n.p5{text-indent:0.44444445in;margin-right:0.03888889in;text-align:right;hyphenate:auto;font-family:仿宋;font-size:16pt;}\n</style>\n<meta content="匿名用户" name="author" />\n\n\n<p class="p1">\n<span class="s1">重庆市南岸区人民法院</span>\n</p>\n<p class="p2">\n<span class="s1">刑事判决书</span>\n</p>\n<p class="p3">\n<span class="s2">                       （2017）渝0108刑初34号</span>\n</p>\n<p class="p4"></p>\n<p class="p4">\n<span class="s2">公诉机关重庆市南岸区人民检察院。</span>\n</p>\n<p class="p4">\n<span class="s2">被告人杜成国，男，1974年9月25日出生，汉族，初中文化，无业，住重庆市南岸区长生镇。2016年11月20日因本案被抓获关押，次日被刑事拘留，同年12月6日被逮捕，现羁押在重庆市南岸区看守所。</span>\n</p>\n<p class="p4">\n<span class="s2">重庆市南岸区人民检察院以渝南检公诉刑诉〔2016〕1305号起诉书指控被告人杜成国犯妨害公务罪，于2017年1月3日向本院提起公诉。本院依法适用简易程序，实行独任审判，于2017年1月10日公开开庭审理了本案。重庆市南岸区人民检察院指派代理检察员顾杰出庭支持公诉，被告人杜成国到庭参加诉讼。现已审理终结。</span>\n</p>\n<p class="p4">\n<span class="s2">公诉机关指控：2016年11月20日11时许，被告人杜成国醉酒后与妻子刘某因家庭锁事发生纠纷，并造成刘某受伤，随后刘某拨打报警电话。当日11时50分左右，民警赵月刚等人出警将杜成国、刘某带至重庆市公安局长生桥派出所进行调解。在调解过程中，被告人杜成国不听民警劝解，无故用拳头殴打民警赵月刚面部，随即其他民警和协勤人员上前对杜成国进行控制，杜成国又继续对民警瞿雪峰、协勤张某某进行殴打，之后，杜成国被民警控制。</span>\n</p>\n<p class="p4">\n<span class="s2">归案后，被告人杜成国如实供述了犯罪事实。</span>\n</p>\n<p class="p4">\n<span class="s2">另查明，民警赵月刚被打后经医院诊断为头面部软组织伤、轻微脑震荡；瞿雪峰经诊断为头部软组织伤。</span>\n</p>\n<p class="p4">\n<span class="s2">公诉机关为此建议对被告人杜成国在有期徒刑七个月至一年七个月范围内予以处罚。</span>\n</p>\n<p class="p4">\n<span class="s2">上述事实，被告人杜成国在审理过程中均无异议。且有证人田贵彬、刘某的证言；出警民警赵月刚、瞿雪峰及协勤张某某的陈述；监控视频等视听资料；辨认笔录；接警记录、归案经过、病历资料、情况说明以及被告人杜成国的供述等证据予以证明。</span>\n</p>\n<p class="p4">\n<span class="s2">本院认为，被告人杜成国因家庭纠纷而由警方介入调解，其使用暴力方法阻碍人民警察依法执行公务，其行为已构成妨害公务罪。控方指控的罪名成立，本院予以支持。</span>\n</p>\n<p class="p4">\n<span class="s2">被告人杜成国公然在公安机关内暴力袭击正在执行职务的警察，应依法从重处罚。鉴于其在归案后能如实供述犯罪事实，有坦白情节，可从轻处罚。据此，依照《中华人民共和国刑法》第二百七十七条第一款、第五款、第六十七条第三款的规定，判决如下：</span>\n</p>\n<p class="p4">\n<span class="s2">被告人杜成国犯妨害公务罪，判处有期徒刑七个月。</span>\n</p>\n<p class="p4">\n<span class="s2">（刑期从判决执行之日起计算，判决执行前先行羁押的，羁押一日折抵刑期一日。即从2016年11月20日至2017年6月19日止）</span>\n</p>\n<p class="p4">\n<span class="s2">如不服本判决，可在接到判决书的第二日起十日内，通过本院或者直接向重庆市第五中级人民法院提出上诉。书面上诉的，应当提交上诉状正本一份，副本二份。</span>\n</p>\n<p class="p4"></p>\n<p class="p4">\n<span class="s2"> </span>\n</p>\n<p class="p4"></p>\n<p class="p3">\n<span class="s2">                        审  判  员    戴  雷</span>\n</p>\n<p class="p4"></p>\n<p class="p4"></p>\n<p class="p4"></p>\n<p class="p5">\n<span class="s2">二○一七年一月十日</span>\n</p>\n<p class="p4"></p>\n<p class="p3">\n<span class="s2">                        书  记  员    张  青</span>\n</p>\n\n\n</div>\n\n\n<dl>\n           <dd>公\xa0\xa0告</dd>\n<dt>一、本裁判文书库公布的裁判文书由相关法院录入和审核，并依据法律与审判公开的原则予以公开。若有关当事人对相关信息内容有异议的，可向公布法院书面申请更正或者下镜。</dt>\n<dt>二、本裁判文书库提供的信息仅供查询人参考，内容以正式文本为准。非法使用裁判文书库信息给他人造成损害的，由非法使用人承担法律责任。</dt>\n<dt>三、本裁判文书库信息查询免费，严禁任何单位和个人利用本裁判文书库信息牟取非法利益。</dt>\n<dt>四、未经许可，任何商业性网站不得建立与裁判文书库及其内容的链接，不得建立本裁判文书库的镜像（包括全部和局部镜像），不得拷贝或传播本裁判文书库信息。</dt>\n</dl>\n</div>\n', 'title': '杜成国妨害公务罪一审刑事判决书', 'court': '重庆市南岸区人民法院', 'pub_date': '2017-11-01'}
    process_ws(items)