import os
import re


def read_config(name):
    with open(os.path.abspath(__file__ + '/../' + "/dict/{}".format(name)), 'r') as f:
        file = f.readlines()
    return sorted([key.strip() for key in file], key=lambda s: len(s), reverse=True)

def read_symbol_config(name):
    p = {}
    with open(os.path.abspath(__file__ + '/../' + "/dict/{}".format(name)), 'r') as f:
        for line in f:
            lines = line.strip().split(',', -1)
            if len(lines) == 3:
                p[lines[0]] = {'identity_type': lines[1], 'identity': lines[2]}
            elif len(lines) == 4:
                p[lines[0]] = {'identity_type': lines[1], 'identity': lines[2], 'party_position': lines[3]}
    return p

def read_cass_config(n1, n2, n3):

    case, case_mapping = {}, {}
    obj = {'xingshi': '刑事案件', 'minshi': '民事案件', 'xingzheng': '行政案件'}
    for n in [n1, n2, n3]:
        cases = []
        case_mappings = {}
        with open(os.path.abspath(__file__ + '/../' + "/dict/{}".format(n)), 'r') as f:
            for line in f:
                lines = line.strip().split(',', -1)
                case_mappings[lines[0]] = {'reason_code': lines[1], 'reason': lines[2]}
                cases.append(lines[0])
        name = obj[n]
        case[name] = cases
        case_mapping[name] = case_mappings
    return case, case_mapping

cases, case_mappings = read_cass_config('xingshi', 'minshi', 'xingzheng')
read_symbol_config('person_mapping')
'''
person部分配置文件
'''
accuse_person = read_config('accuse_person')
court_person = read_config('court_person')
case_person = read_config('case_person')
agent_person = read_config('agent_person')
person_mapping = read_symbol_config('person_mapping')

"""人员关键词"""
key_person = ["审理终结", "一案"]

"""案由所在段落关键词"""
case_keys = read_config('case_keys')

'''
文书类型   
'''
ws_type_title = ['判决书', '裁定书', '调解书', '决定书', '通知书', '支付令']
ws_type_article = {'判决如下': '判决书', '裁定如下': '裁定书', '决定如下': '决定书'}

'''案由'''
case = read_config('case')



def reg():
    regNos = []
    reg1 = '({role})(?:[(（].*?[）)])?(.*)'.format(role='|'.join(agent_person))
    reg2 = '^({role})(?:[(（].*?[）)])?(.*)'.format(role='|'.join(case_person))

    regNos.append(reg1)
    regNos.append(reg2)
    return regNos

def court_reg():
    reg = '(^({})(.*))'.format('|'.join([k for k in court_person]))
    return reg


