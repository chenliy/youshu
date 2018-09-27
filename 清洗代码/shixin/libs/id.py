import hashlib

def get_md5(s):
    """get md5 value
    Args
        s: a bytes, can be None
    Returns
        h.hexdigest(): md5(s) value, 32 bit.
    """
    if s:
        h = hashlib.md5()
        h.update(s)
        return h.hexdigest()
    else:
        return ''

default_time = '1900-01-01'
if __name__ == '__main__':
    print(get_md5(b'\xe7\x89\x9b\xe6\xb2\xbb\xe4\xbc\x9f(2015)\xe9\xba\xa6\xe6\xb3\x95\xe6\x89\xa7\xe5\xad\x97\xe7\xac\xac10\xe5\x8f\xb7'))
