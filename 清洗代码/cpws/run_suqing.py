# coding=utf-8
from IKEA.cpws.pro.caipanwenshu import cpws_article
from IKEA.cpws.pro.caipanwenshu import cpws_list
from IKEA.cpws.wenshu.base import WenshuBase
from IKEA.cpws.qingxi import court_extract
from IKEA.cpws.qingxi import content_type_extract
from IKEA.cpws.qingxi import reason_extract
from IKEA.cpws.qingxi import local_person
from IKEA.cpws.qingxi import type_extract
from IKEA.cpws.qingxi import litigants_agent_extract
from IKEA.cpws.qingxi import court_level_extract
from IKEA.cpws.qingxi import trial_round_extract
from IKEA.cpws.qingxi import claim_extract
from IKEA.cpws.qingxi import trial_date_extract
from IKEA.es.postelastic import ines
from IKEA.cpws.libs.process import process_bracket as pbracket
from IKEA.libs.date import update_time
from IKEA.libs.id import get_md5
from IKEA.es.postelastic import ines
from IKEA.es.postelastic import is_exists
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
def mining(items):
    obj = {}
    a = items.get('articles')
    articles = eval(items.get('articles')) if a else []
    article = '\n'.join(articles)
    title = items.get('title')

    # 必须包括的
    obj['case_no'] = items.get('case_no', '')
    obj['publish_date'] = items.get('publish_date')
    obj['court_name'] = items.get('court_name', '')
    obj['source'] = items.get('source')
    obj['title'] = items.get('title', '')
    obj['update_time'] = update_time()
    obj['org_url'] = items.get('org_url')

    # 可能不在, 自己提取
    obj['type'] = items.get('type') if items.get('type') else type_extract(title)
    obj['trial_round'] = items.get('trial_round') if items.get('trial_round') else trial_round_extract(title)
    obj['content_type'] = content_type_extract(content_type=items.get('content_type')) if items.get(
        'content_type') else None
    content_type = items.get('content_type')
    reason = items.get('reason')
    trial_date = items.get('trial_date')
    if articles:
        ws = WenshuBase(article)
        litigants, agents = litigants_agent_extract('\n'.join(ws.role_paragraph))
        court_officers = court_extract('\n'.join(ws.court_paragraph))
        # print(ws.claims_paragraphs)
        claim = claim_extract(ws.claims_paragraphs)
        trial_date = trial_date if trial_date else trial_date_extract(''.join(ws.court_paragraph))
        court_level = court_level_extract(obj.get('court_name'))
        obj['litigants'] = litigants
        obj['agents'] = agents
        obj['court_officers'] = court_officers
        obj['court_level'] = court_level
        obj['content'] = '<br>'.join(articles)
        obj['content_type'] = content_type if content_type else content_type_extract(verdict=ws.verdict_paragraph,
                                                                                     title=obj.get('title'))
        obj['reasons'] = reason_extract(ws.reason_description, obj.get('title'), obj.get('type'), reason)
        obj['verdict'] = ws.verdict
        obj['trial_date'] = trial_date
        obj['claim'] = claim
    obj['instrument_id'] = get_md5(obj.get('title')) + get_md5(pbracket(obj.get('case_no')))
    return obj

def process_ws(items):
    try:
        obj = mining(items)
        ines(id=obj['instrument_id'], path='http://10.1.1.28:9200/judge_doc/local_doc', data=obj)
        if is_exists(url='http://10.1.1.28:9200/judge_doc/total_doc', field='case_no', value=obj['case_no']):
            ines(id=obj['instrument_id'], path='http://10.1.1.28:9200/judge_doc/total_doc', data=obj)
    except Exception as e:
        id = get_md5(items.get('title')) + get_md5(pbracket(items.get('case_no', '')))
        obj = {
               "_reason_": str(e),
               "data_size": len(items),
               "crawl_time": update_time(),
               "processed": False,
               "hostname": "worker1.yscredit.com",
               "data": items,
               "create_time": update_time(),
               "ip": "null",
               "_id_": id,
               "topic": "裁判文书"
            }
        print(obj)
        ines(id=id, path='http://10.1.1.28:9200/fail_record/fail_record', data=obj)

def claim_extract(claim_paragraphs):
    if not claim_paragraphs:
        return ''
    claims = []
    claim_paragraph = claim_paragraphs[0]
    for claim_sentence in claim_paragraph.split('。'):
        if ('请求' in claim_sentence or '要求' in claim_sentence or '诉请' in claim_sentence) and ('元' in claim_sentence or '万元' in claim_sentence):
            claims.append(claim_sentence)
            return claims
    for claim_sentence in claim_paragraph.split('。'):
        if '诉称' in claim_sentence and ('元' in claim_sentence or '万元' in claim_sentence):
            claims.append(claim_sentence)
            return claims
    claim_paragraph = claim_paragraphs[-1]
    for claim_sentence in claim_paragraph.split('。'):
        if ('请求' in claim_sentence or '要求' in claim_sentence or '诉请' in claim_sentence) and ('元' in claim_sentence or '万元' in claim_sentence):
            claims.append(claim_sentence)
            return claims
    return ''

def suqing(article):
    article = article.replace('<br>', '\n')
    ws = WenshuBase(article)
    c = claim_extract(ws.claims_paragraphs)

    return ''.join(c).replace('\n', '')



if __name__ == '__main__':
    import requests
    import json
    SIZE = 200
    size = 200
    f = open('claims', 'a')
    for i in range(SIZE):
        query = {
            "from": i*size, "size": size,
            "query": {
              "bool": {
                  "must": {"exists": {"field": "claim"}},
                  "must_not": [{"term": {"reasons.reason.keyword": {"value": "离婚纠纷"}}}]
              }
            }
        }
        print(i)
        html = requests.get('http://10.20.20.105:9200/judge_doc/total_doc/_search', json=query)
        for item in json.loads(html.text)['hits']['hits']:
            article = item['_source']['content']
            v = suqing(article)
            if v:
                print(v)
                f.write(v + '\n')