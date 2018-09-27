# coding:utf-8
from IKEA.cpws.config import reg
from IKEA.cpws.config import court_reg
from IKEA.cpws.config import agent_person
from IKEA.cpws.config import case_person
from IKEA.cpws.config import person_mapping
from IKEA.cpws.config import ws_type_article
from IKEA.cpws.config import ws_type_title
from IKEA.cpws.config import cases
from IKEA.cpws.config import case_mappings
from IKEA.cpws.libs.process import process_birthday as pb
from IKEA.cpws.libs.process import process_symbol as ps
from IKEA.cpws.libs.process import process_remark as pr
from IKEA.cpws.libs.process import process_bracket as pbracket
from IKEA.cpws.libs.litigants import name_clear
from IKEA.cpws.libs.litigants import is_person
from IKEA.cpws.libs.claims import claims_money
from datetime import date
from operator import itemgetter
import copy
import re

data_dict = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '0': 0,
    '〇': 0,
    'o': 0,
    'О': 0,
    '○': 0,
    'O': 0,
    '零': 0,
    '元': 1,
    '一': 1,
    '二': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '六': 6,
    '七': 7,
    '八': 8,
    '九': 9,
    '十': 10,
    '年': '年',
    '月': '月',
    '日': '日'
}



def exchange_y_z(string):
    string = ''.join([s for s in string if s in data_dict.keys()])
    if string:
        d = [data_dict.get(s, 0) for s in string]
    else:
        d = [0]
    if d == [10]:
        return 10
    elif len(d) == 2 and d[0] == 10:
        return 10 + d[1]
    elif len(d) == 2 and d[1] == 10:
        return d[0] * 10
    elif len(d) == 3 and d[1] == 10:
        del d[1]
    if len(d) == 1:
        return d[0]
    else:
        return d[0] * 10 + d[1]


"""先提取名字简介和角色
"""


def person_extract(role_paragraph):
    """采集当事人和代理人员信息
    """
    regs = reg()
    persons = []
    role_paragraphs = role_paragraph.split('\n')
    del_paragraphs = [rp for rp in role_paragraphs if ('执行裁定书' or '执行决定书' or '执行通知书') in rp]
    for dp in del_paragraphs:
        role_paragraph = role_paragraph.replace(dp, '')
    role_paragraphs = role_paragraph.split('\n')

    for num, r in enumerate(regs):
        for items in re.findall(r, role_paragraph, re.M):
            identity_type, identity, party_position = '', '', ''
            role = items[0]
            sentence = items[1]
            if (')' in sentence or '）' in sentence) and ('(' not in sentence or '（' not in sentence) and num == 0:
                pass
            else:
                if sentence:
                    _sentence = sentence[1:] if sentence[0] in [',', '，', '。', '.', ';', '；', '∶'] else sentence
                    symbols = list(set([_sentence.find(i) for i in [',', '，', '。', '.', ';', '；']]))
                    symbols.remove(-1)
                    symbols = sorted(symbols)
                    if symbols:
                        _name = ps(_sentence[:symbols[0]])
                        resume = _sentence[symbols[0]:]
                        resume = resume[1:] if resume[0] in [',', '，', '。', '.', ';'] else resume
                    else:
                        _name = ps(_sentence)
                        resume = ''

                    bir = pb(resume)
                    i = pr(_name) if _name else None
                    if i:
                        name = _name[:i]
                        remark = _name[i:]
                    else:
                        name = _name
                        remark = ''

                    law_firm_sentence = re.findall("[,，。.;；](.*?(?:律师事务所|法律服务所))", resume)
                    law_firm_sentence = law_firm_sentence[0] if law_firm_sentence else resume
                    law_firm = re.findall("系?(.*?(?:律师事务所|法律服务所))", law_firm_sentence)
                    law_firm = law_firm[0] if law_firm else ''

                    s = [t for t in role_paragraphs if sentence in t][0]
                    local = role_paragraphs.index(s)
                    role_paragraphs[local] = ''
                    role_paragraph = '\n'.join(role_paragraphs)

                    if role:
                        identity_type, identity, party_position = person_mapping[role].get('identity_type'), \
                                                                  person_mapping[
                                                                      role].get('identity'), person_mapping[role].get(
                            'party_position', '')
                    persons.append(
                        {'name': pbracket(name), 'local': local, 'resume': resume, 'role': role, 'sentence': s,
                         'bir': bir,
                         'remark': remark, 'identity_type': identity_type, 'identity': identity,
                         'party_position': party_position, 'law_firm': pbracket(law_firm)})
    persons = sorted(persons, key=lambda x: x['local']) if persons else [
        {'name': p, 'local': 0, 'resume': '', 'role': '', 'sentence': ''} for p in
        re.findall('(.*?)[:：,，;；]$', role_paragraph, re.M)]

    return persons


def local_person(persons):
    _persons = copy.copy(persons)
    for person in persons:
        location = ''
        n = _persons.index(person)
        if person.get('identity_type', '') == '代理人':
            if '共同' not in person['resume']:
                location = _persons[n - 1]['name']
            else:
                r = _persons[n - 1]['identity_type']
                for p in reversed(_persons[:n]):
                    if p['identity_type'] == r:
                        location += p['name']
                    else:
                        break
            del _persons[n]
        person['location'] = location

    return persons


def map_person(persons):
    litigants, agents = [], []
    for p in persons:
        if p.get('identity_type', '') == "当事人":
            name = name_clear(p.get("name", ''))
            litigant = {
                "name": name,
                "identity": p.get("identity", ''),
                "birth_date": p.get("bir", ''),
                "identity_type": "当事人",
                "status": p.get('party_position', ''),
                "name_id": "",
                "type": is_person(name),
                "card_num": "",
                "position": "",
                "brief_introduction": p.get('resume', ''),
                "name_backup": p.get('remark', '')
            }
            litigants.append(litigant)
        elif p.get('identity_type', '') == "代理人":
            agent = {
                "name": p.get("name", ''),
                "identity": p.get("identity", ''),
                "name_id": "",
                "law_office": p.get('law_firm', ''),
                "brief_introduction": p.get('resume', ''),
                "position": p.get('location', '')
            }
            agents.append(agent)
    return litigants, agents


def litigants_agent_extract(role_paragraph):
    return map_person(local_person(person_extract(role_paragraph)))


def court_extract(court_paragraph):
    """采集法院人员信息"""
    courts = []
    regNo = court_reg()
    court_paragraphs = court_paragraph.split('\n')
    for items in re.findall(regNo, court_paragraph, re.M):
        identity_type, identity, party_position = '', '', ''
        sentence = items[0]
        role = items[1]
        name = ps(items[2])
        if role:
            identity_type, identity, party_position = person_mapping[role].get('identity_type'), person_mapping[
                role].get('identity'), person_mapping[role].get('party_position', '')
        courts.append({'name': name, 'identity': identity})
    return courts


def content_type_extract(verdict='', title='', content_type=None):
    if content_type:
        for ws in ws_type_title:
            if ws in content_type:
                return ws
    content_types = [ws_type_article[ws] for ws in ws_type_article.keys() if ws in verdict] if verdict else [ws for ws
                                                                                                             in
                                                                                                             ws_type_title
                                                                                                             if
                                                                                                             ws in title]
    return content_types[0] if content_types else ''


# 提取案由
def reason_extract(reason_description='', title='', trial_type='', reason=''):
    reasons = []
    case_source = []
    _reason_description = copy.copy(reason_description)
    case = sorted(cases.get(trial_type, ''), key=lambda s: len(s), reverse=True)
    case_mapping = case_mappings.get(trial_type, '')

    if case:
        for c in case:
            if c in reason_description:
                reason_description = re.sub(c, '', reason_description)
                case_source.append(c)
        if len(case_source) == 0:
            for c in case:
                if c in title:
                    title = re.sub(c, '', title)
                    case_source.append(c)
        if len(case_source) == 0:
            for c in case:
                if c in reason:
                    case_source.append(c)
        if len(case_source) == 0:
            case_source = ['默认']
        reasons = [{
            "reason": case_mapping[cs]['reason'],
            "reason_description": _reason_description,
            "reason_code_level1": int(int(case_mapping[cs]['reason_code']) / 100000000),
            "reason_code_level2": int(int(case_mapping[cs]['reason_code']) / 1000000),
            "reason_code_level3": int(int(case_mapping[cs]['reason_code']) / 10000),
            "reason_code_level4": int(int(case_mapping[cs]['reason_code']) / 100),
            "reason_code_level5": case_mapping[cs]['reason_code']
        } for cs in set(case_source)]
    return reasons


def court_level_extract(s):
    """ 根据法院名称判断法院层级
    Args
        s: 法院名称
    Returns
        法院层级
    """
    special_law = ['军事法院', '海事法院', '铁路运输法院', '森林法院', '农垦法院', '石油法院', '林区基础法院', '林区中级法院', '矿区人民法院']
    if '最高' in s:
        return '最高法院'
    elif '高级' in s:
        return '高级法院'
    elif '中级' in s or '知识产权' in s:
        return '中级法院'
    elif True in [key in s for key in special_law]:
        return '专门法院'
    else:
        return '基层法院'


def trial_date_extract(court_paragraphs):
    for num in range(len(court_paragraphs)):
        court_paragraph = court_paragraphs[num].replace(' ', '')
        if court_paragraph == '':
            continue
        exist = False
        for d in court_paragraph:
            if d not in data_dict.keys():
                exist = True
                break
        if not exist:
            d = re.findall('(.{2})年(.{1,3})月(.{1,3})日', court_paragraph)
            d = d[-1] if d else []
            if len(d) == 3:
                year = 2000 + exchange_y_z(d[0])
                month = exchange_y_z(d[1])
                day = exchange_y_z(d[2])
                if month == 0 or day == 0:
                    break
                return date(year, month, day).isoformat()
    return ''



def type_extract(title):
    if '刑事' in title:
        type = '刑事案件'
    elif '民事' in title and '刑事' not in title:
        type = '民事案件'
    elif '行政' in title and '赔偿' not in title:
        type = '行政案件'
    elif '赔偿' in title:
        type = '赔偿案件'
    elif '执行' in title:
        type = '执行案件'
    else:
        type = ''
    return type


def trial_round_extract(title):
    trial_round_keys = ['一审', '二审', '非诉执行审查', '其他', '刑罚变更', '非诉执行审查', '再审审查与审判监督',
                        '特别程序', '复核', '减刑假释', '申诉', '赔偿', '刑法变更']
    for key in sorted(trial_round_keys, key=lambda a: len(a), reverse=True):
        if key in title:
            return key


def claim_extract(claim_paragraphs):
    if not claim_paragraphs:
        return '', ''
    claim_paragraph = claim_paragraphs[0]
    for claim_sentence in claim_paragraph.split('。'):
        if ('请求' in claim_sentence or '要求' in claim_sentence or '诉请' in claim_sentence) and ('元' in claim_sentence or '万元' in claim_sentence):
            return claim_sentence, claims_money(claim_sentence)
    for claim_sentence in claim_paragraph.split('。'):
        if '诉称' in claim_sentence and ('元' in claim_sentence or '万元' in claim_sentence):
            return claim_sentence, claims_money(claim_sentence)
    claim_paragraph = claim_paragraphs[-1]
    for claim_sentence in claim_paragraph.split('。'):
        if ('请求' in claim_sentence or '要求' in claim_sentence or '诉请' in claim_sentence) and ('元' in claim_sentence or '万元' in claim_sentence):
            return claim_sentence, claims_money(claim_sentence)
    return '', ''


if __name__ == '__main__':
    a = '一七年十一月十四无'
    print(trial_date_extract(a))