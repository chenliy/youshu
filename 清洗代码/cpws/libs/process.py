import re
from datetime import date

def process_symbol(text):
    """process all symbol.such , . ， 。 ...
    """
    punct = set(u''':!,.:;?]}¢'"。〉》」』】〕〗〞︰︱︳﹐､﹒
    ﹔﹕﹖﹗﹜﹞！，：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
    々‖•·ˇˉ―--′’”[{£¥'"‵〈《「『【〔〖［｛￡￥〝︵︷︹︻
    ︽︿﹁﹃﹛﹝｛“‘-—_''')
    pp = sorted([text.find(p) for p in punct])
    return text[pp[-1]+1:] if pp else text

def process_html(text):
    """process all html tag
    """
    return re.sub(r'<[^>]+>', '', text)

def process_english(text):
    """processs all englist
    """
    return re.sub(r'^[a-zA-Z]', '', text)

def process_birthday(s):
    try:
        reg = '([12]\d{3})[-_—/年](\d{1,2})[-_—/月](\d{1,2})日?(?:出生|生)'
        birthday = re.findall(reg, s, re.M)
        birthday = birthday[0] if birthday else []
        d = date(int(birthday[0]), int(birthday[1]), int(birthday[2])).strftime("%Y%m%d") if len(birthday) == 3 else ''
    except:
        d = None
    return d

def process_remark(s):
    i = []
    if s[-1] == ')':
        i = [pos for pos, char in enumerate(s) if char == '(']
    if s[-1] == '）':
        i = [pos for pos, char in enumerate(s) if char == '（']
    if i:
        i = sorted(i)
        return i[-1]

def process_t(s):
    return re.sub('\n', '', re.sub('\t', '', s))

def process_bracket(s):
    if ')' in s or '(' in s:
        s = s.replace('(', '（').replace(')', '）')
    return s


