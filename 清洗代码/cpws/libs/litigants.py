import sys
import requests
import re


def name_clear(name):
    if True in [True for key in ['纠纷', '申请', '罪', '根据', '作出', '因与', '为与'] if key in name] or len(name) > 3 and True in [
        True for key in ['查明', '作为'] if key in name] or len(name) > 5 and name.startswith('以') or name.endswith(
            '纠') or name == '称':
        return ''
    # 开头去数字
    digit_name = [n for n, i in enumerate(name) if i.isdigit()]
    _digit_name = [d for n, d in enumerate(digit_name) if d == n]
    name = name[_digit_name[-1] + 1:] if _digit_name else name
    # 去除部分标签
    name = re.sub("('&&|&#|&#xB;|&Auml|&bull|&ensp|&hellip|&middot|&times|&[A-Za-z]*)", '', name)
    # 处理大括号
    symbol_name = sorted(
        [name.index(symbol) for symbol in ['】', ']', '］'] if symbol in name and name.endswith(symbol) is False])
    name = name[symbol_name[-1] + 1:] if symbol_name else name
    # 去除身份关键词
    role_name = sorted(
        [name.index(key) + len(key) for key in ['原告', '原告人', '上诉人', '被告', '被告人', '申请人', '罪犯', '犯罪嫌疑人', '公诉机关', '抗诉机关']
         if key in name])
    name = name[role_name[-1]:] if role_name else name
    # 处理括号
    bracket_name = sorted([name.index(i) for i in [')', '(', '）', '（'] if i in name])
    if len(bracket_name) == 1 and (bracket_name[0] == 0 or bracket_name[0] == len(name) - 1):
        name = name.replace(name[bracket_name[0]], '')
    elif len(bracket_name) == 1:
        name = name[bracket_name[0] + 1:] if name[bracket_name[0]] in [')', '）'] else name[:bracket_name[0]]
    elif len(bracket_name) == 2:
        if bracket_name[0] == 0:
            name = name[bracket_name[-1] + 1:]
        elif bracket_name[-1] == len(name) - 1:
            if '合伙' in name[bracket_name[0]:]:
                name = name
            else:
                name = name[:bracket_name[0]]
        else:
            if '检察院' not in name:
                if '以下简称' in name[bracket_name[0]:bracket_name[1] + 1] or '下称' in name[bracket_name[0]:bracket_name[
                    1] + 1] or '曾用名' in name[bracket_name[0]:bracket_name[1] + 1]:
                    name = name[:bracket_name[0]] + name[bracket_name[1] + 1:]
    return name


# http://master2:5000
def is_person(text):
    if len(text) <= 3:
        return str(1)
    elif len(text) >= 4 and ('公司' in text or '有限合伙' in text):
        return str(3)
    elif len(text) >= 4 and text.endswith('厂'):
        return str(3)
    else:
        # http://10.20.20.105:5000/is_person_or_org?name=name http://10.1.1.28:5000/is_person_or_org?name=name
        url = r'http://10.1.1.28:5000/is_person_or_org?name={}'.format(text)
        page = requests.get(url)
    return page.text




if __name__ == '__main__':
    text = '汪峰'
    url = r'http://10.1.1.28:5000/{}'.format(text)

    page = requests.get(url)
    print(page.text)
