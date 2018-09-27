import hashlib

def get_md5(s):
    """get md5 value
    Args
        s: a bytes, can be None
    Returns
        h.hexdigest(): md5(s) value, 32 bit.
    """
    if s:
        key = bytes(s, encoding='utf-8')
        h = hashlib.md5()
        h.update(key)
        return h.hexdigest()
    else:
        return ''

default_time = '1900-01-01'
if __name__ == '__main__':
    print(get_md5('adsadasdf'))