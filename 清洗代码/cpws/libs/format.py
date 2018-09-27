import re
from datetime import datetime


def RoleFormat(dics):
    """format role to show

    :return {role}-{name}-{resume}-{local}
    """
    _list = []
    for dic in dics:
        name, resume, role, local = dic.get('name', ''), dic.get('resume', ''), dic.get('role', ''), dic.get('local', '')
        _str = '{role}    {name}    {resume}    {local}'.format(role=role, name=name, resume=resume,  local=local)    # change show format
        _list.append(_str)
    return _list

def html_format(detail_response):
    """add lost html

    :return detail_response
    """
    return re.sub('u003e', '\u003e', re.sub('u003c', "\u003c", detail_response))

