from IKEA.cpws.pro.caipanwenshu import cpws_article
from IKEA.cpws.pro.caipanwenshu import cpws_list
from IKEA.mysql.mysqlbase import MysqlBase
from IKEA.cpws.wenshu.base import WenshuBase
from IKEA.cpws.qingxi import court_extract
from IKEA.cpws.qingxi import content_type_extract
from IKEA.cpws.qingxi import reason_extract
from IKEA.cpws.qingxi import local_person
from IKEA.cpws.qingxi import litigants_agent_extract
from IKEA.cpws.qingxi import court_level_extract
from IKEA.cpws.qingxi import claim_extract
from IKEA.es.postelastic import ines
from IKEA.cpws.libs.process import process_bracket as pbracket
from IKEA.libs.date import update_time
from IKEA.config import p_connecter as connecter
from IKEA.es.postelastic import is_ws_exists
import json


# 测试环境
crawl_connecter = {
    'host': '10.1.1.30',
    'user': 'root',
    'password': 'root',
    'db': 'test'
}

def process_ws(items):
    article = cpws_article(items)
    obj = {}
    cpws_lists = cpws_list(items)
    obj['instrument_id'] = cpws_lists.get('instrument_id')
    obj['court_name'] = cpws_lists.get('court_name')
    obj['type'] = cpws_lists.get('trial_type')
    obj['trial_round'] = cpws_lists.get('trial_round')
    obj['trial_date'] = cpws_lists.get('trial_date')
    obj['title'] = cpws_lists.get('title')
    obj['case_no'] = cpws_lists.get('case_no')
    obj['source'] = '裁判文书网'
    obj['update_time'] = update_time()
    obj['operator'] = 'leifeng'
    if article == '无全文':
        obj['has_content'] = False
    try:
        if article and article != '无全文':
            ws = WenshuBase(article)
            litigants, agents = litigants_agent_extract('\n'.join(ws.role_paragraph))
            court_officers = court_extract('\n'.join(ws.court_paragraph))
            # print(ws.claims_paragraphs)
            claim = claim_extract(ws.claims_paragraphs)
            obj['litigants'] = litigants
            obj['agents'] = agents,
            obj['court_officers'] = court_officers
            obj['court_level'] = court_level_extract(cpws_lists.get('court_name'))
            obj['publish_date'] = eval(items['detail_response'])['PubDate'] if '{' in items['detail_response'] else ''
            obj['content'] = ws.article
            obj['content_type'] = content_type_extract(verdict=ws.verdict_paragraph, title=cpws_lists.get('title'))
            reasons = reason_extract(ws.reason_description, cpws_lists.get('title'), cpws_lists.get('trial_type'))
            obj['reasons'] = reasons
            obj['verdict'] = ws.verdict
            obj['claim'] = claim
    except:
        pass
    return obj


if __name__ == '__main__':
    item ={}
    l = "{'案件类型': '2', '案件名称': '杨明芝与席文广合同纠纷一审民事裁定书', '文书ID': '84123dd1-fbe1-487a-b7f7-a74001110d9c', '法院名称': '郑州市金水区人民法院', '裁判日期': '2017-01-22', '案号': '（2017）豫0105民初1788号', '审判程序': '一审'}"
    item['list_response'] = l
    item['detail_response'] = """{"Title":"杨明芝与席文广合同纠纷一审民事裁定书","PubDate":"2017-03-24","Html":"\u003ca type=\u0027dir\u0027 name=\u0027WBSB\u0027\u003e\u003c/a\u003e\u003cdiv style=\u0027TEXT-ALIGN: center; LINE-HEIGHT: 25pt; MARGIN: 0.5pt 0cm; FONT-FAMILY: 宋体; FONT-SIZE: 22pt;\u0027\u003e河南省郑州市金水区人民法院\u003c/div\u003e\u003ca type=\u0027dir\u0027 name=\u0027SSJL\u0027\u003e\u003c/a\u003e\u003cdiv style=\u0027TEXT-ALIGN: center; LINE-HEIGHT: 30pt; MARGIN: 0.5pt 0cm; FONT-FAMILY: 仿宋; FONT-SIZE: 26pt;\u0027\u003e民 事 裁 定 书\u003c/div\u003e\u003cdiv style=\u0027TEXT-ALIGN: right; LINE-HEIGHT: 30pt; MARGIN: 0.5pt 0cm;  FONT-FAMILY: 仿宋;FONT-SIZE: 16pt; \u0027\u003e（2017）豫0105民初1788号\u003c/div\u003e\u003cdiv style=\u0027LINE-HEIGHT: 25pt;TEXT-ALIGN:justify;TEXT-JUSTIFY:inter-ideograph; TEXT-INDENT: 30pt; MARGIN: 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;\u0027\u003e原告杨明芝，女，1971年5月26日出生，住郑州市金水区。\u003c/div\u003e\u003cdiv style=\u0027LINE-HEIGHT: 25pt;TEXT-ALIGN:justify;TEXT-JUSTIFY:inter-ideograph; TEXT-INDENT: 30pt; MARGIN: 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;\u0027\u003e委托代理人王德福、魏雷明，河南千诺律师事务所律师。\u003c/div\u003e\u003cdiv style=\u0027LINE-HEIGHT: 25pt;TEXT-ALIGN:justify;TEXT-JUSTIFY:inter-ideograph; TEXT-INDENT: 30pt; MARGIN: 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;\u0027\u003e被告席文广，男，1978年3月8日出生，汉族，住河南省南召县。\u003c/div\u003e\u003cdiv style=\u0027LINE-HEIGHT: 25pt;TEXT-ALIGN:justify;TEXT-JUSTIFY:inter-ideograph; TEXT-INDENT: 30pt; MARGIN: 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;\u0027\u003e本院在审理原告杨明芝与被告席文广合同纠纷一案中，因原告未在本院指定的期限内预交诉讼费用，也未申请缓、减、免。依照《中华人民共和国民事诉讼法》第一百一十八条、第一百五十四条第一款第十一项、《诉讼费用交纳办法》第二十二条第一、四款并参照《最高人民法院关于适用\u003c中华人民共和国民事诉讼法\u003e的解释》第二百一十三条规定，裁定如下：\u003c/div\u003e\u003ca type=\u0027dir\u0027 name=\u0027PJJG\u0027\u003e\u003c/a\u003e\u003cdiv style=\u0027LINE-HEIGHT: 25pt;TEXT-ALIGN:justify;TEXT-JUSTIFY:inter-ideograph; TEXT-INDENT: 30pt; MARGIN: 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;\u0027\u003e本案按撤诉处理。\u003c/div\u003e\u003ca type=\u0027dir\u0027 name=\u0027WBWB\u0027\u003e\u003c/a\u003e\u003cdiv style=\u0027TEXT-ALIGN: right; LINE-HEIGHT: 25pt; MARGIN: 0.5pt 72pt 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;\u0027\u003e审判员　　李楠楠\u003c/div\u003e\u003cbr/\u003e\u003cdiv style=\u0027TEXT-ALIGN: right; LINE-HEIGHT: 25pt; MARGIN: 0.5pt 72pt 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;\u0027\u003e二〇一七年一月二十二日\u003c/div\u003e\u003cdiv style=\u0027TEXT-ALIGN: right; LINE-HEIGHT: 25pt; MARGIN: 0.5pt 72pt 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;\u0027\u003e书记员　　高路航\u003c/div\u003e"}"""
    print(process_ws(item))


