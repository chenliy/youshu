from pyquery import PyQuery as pq
import re
import json
from IKEA.cpws.libs.process import process_html as ph

def html_format(detail_response):
    """add lost html

    :return detail_response
    """
    return re.sub('u003e', '\u003e', re.sub('u003c', "\u003c", detail_response))

def cpws_article(items):
    if '}' in items['detail_response']:
        detail_response = html_format(eval(items['detail_response'])['Html'])
        articles = [ph(text.strip()) for text in re.findall('<div.*?>(.*?)</div>', detail_response)]
        articles = [re.sub(' ', '', re.sub('\u3000', '', re.sub('\n', '', article))) for article in articles][3:]
        return '\n'.join(articles)
    else:
        return items['detail_response']


def cpws_list(items):
    l = eval(items['list_response'])
    CASE_TYPE_MAP = {"0": "", "1": "刑事案件", "2": "民事案件", "3": "行政案件", "4": "赔偿案件", "5": "执行案件",
                     "执行案件": "执行案件", "赔偿案件": "赔偿案件", "民事案件": "民事案件", "刑事案件": "刑事案件", "行政案件": "行政案件"}
    return {
        'case_no': l.get('案号'),
        'title': l.get('案件名称'),
        'trial_round': l.get("审判程序"),
        'instrument_id': l.get("文书ID"),
        'court_name': l.get("法院名称"),
        'trial_date': l.get('裁判日期'),
        'trial_type': CASE_TYPE_MAP[l.get('案件类型', '0')]
    }
