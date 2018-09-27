

def itype(kwargs):
    if kwargs.get('itype'):
        if kwargs['itype'] == '自然人':
            kwargs['itype'] = 1
        elif kwargs['itype'] == "法人":
            kwargs['itype'] = 3
        else:
            kwargs['itype'] = 2
    return kwargs