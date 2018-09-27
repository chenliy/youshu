import requests
import json
import re

def claims_money(claims):
    # http://10.20.20.105:5000/is_person_or_org?name=name http://10.1.1.28:5000/is_person_or_org?name=name
    # url = 'http://10.1.1.28:5000/extractInvolvedAmount'
    url = 'http://10.10.10.143:7776/predict'
    data = {
        'content': claims
    }
    html = requests.post(url, data=data)
    json_moneys = json.loads(html.text)
    entities = json_moneys.get('entities', [])
    claim = 0.0
    for num in range(len(entities)):
        claim_single = entities[num].get('word', '')
        claim = claim + float(re.sub('[美]?元', '', claim_single))
    return round(claim, 2)

if __name__ == '__main__':
    pass