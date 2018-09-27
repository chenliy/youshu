import requests
import json
from datetime import datetime


def ines(id, path, data):
    for d in data:
        if data[d] == '' or data[d] == 'null':
            data[d] = None
    data = json.dumps(data)
    url = '{}/{}'.format(path, 'e_' + id)
    html = requests.post(url, data=data)
    print('{}:result={}:{}'.format(datetime.now(), html.status_code, url))
    print(html.text)



def count(url, field, value):
    """count field: value num in url es
    Args
        url: host/index/type
        field: field in es
        value: str value
    """
    page = requests.request('get', '{}/_count'.format(url),
                            json={"query": {"term": {field: value}}})
    return json.loads(page.text)['count']


def is_exists(url, field, value):
    """
    Returnx
        bool: exists False & not exists True
    """
    if value == '' or not value:
        return True
    return True if count(url, field, value) == 0 else False

# 昨天之前, content null case_no
def is_ws_exists(case_no):
    data = {
        "query": {
            "bool": {
                "must_not": [
                    {"term": {"source": {"value": "裁判文书网"}}}
                ],
                "must": [
                    {"term": {"case_no": {"value": case_no}}}
                ]
            }
        }
    }
    # http://10.20.20.105:9200  http://10.1.1.28:9200
    page = requests.request('post', 'http://10.20.20.105:9200/judge_doc/total_doc/_search', json=data)
    return True if int(json.loads(page.text)['hits']['total']) == 0 else False

def is_ws_exists2(keyword, instrument_ids):
    data = {
        "from": 0, "size": 220,
        "_source": "instrument_id",
        "query": {"nested": {
          "path": "litigants",
          "query": {
            "bool": {
              "must": [
                {"term": {"litigants.name.keyword": {"value": keyword}}}

              ],
              "must_not": [
                {"range": {"update_time": {"lt": "now-1h"}}},
                {"term": {"has_content": {"value": "false"}}}
              ]
            }
          }
        }}
    }
    page = requests.request('post', 'http://10.20.20.105:9200/judge_doc/wenshuwang_doc/_search', json=data)
    # page = requests.request('post', 'http://10.1.1.28:9200/judge_doc/wenshuwang_doc/_search', json=data)

    right_instrument_ids = set([hits['_source']['instrument_id'] for hits in json.loads(page.text)['hits']['hits']])
    return set(instrument_ids) - set(right_instrument_ids)


if __name__ == '__main__':
    s = is_ws_exists2('杭州广厦木业有限公司', ['1d57cce7-907a-481a-8444-dbee21fa3d5a','a77fe986-7bca-4136-906c-265b048a331f',"1064ea20-a3c3-4bb1-baf9-6c6ab47c0e8f", "3604f37c-ac8d-4731-9d0a-76435483e353","87c891df-4a90-40de-a54a-119bd37b5b8d","87bd7ed7-4600-413d-8e1f-f75558a62f57","5bb3797f-34f3-4be1-a8a4-dfbe4ff85860", "d253974a-0452-4961-a7e0-ddca45dc7249","b53c440b-601e-4307-b4f7-6f5abefff8dc", "fba5797f-ab28-4a07-9d9f-4a1f220c38b7","c699776d-40bf-493a-aaf0-ad3e4ffdeedb"])
    print(s)