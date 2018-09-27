
have = []
with open('/home/maybe/judiciary/python/IKEA/cpws/dict/minshi', 'r') as f:
    reason = f.readlines()
have = have + [r.split(',')[0] for r in reason]
with open('/home/maybe/judiciary/python/IKEA/cpws/dict/xingshi', 'r') as f:
    reason = f.readlines()
have = have + [r.split(',')[0] for r in reason]
with open('/home/maybe/judiciary/python/IKEA/cpws/dict/xingzheng', 'r') as f:
    reason = f.readlines()
have = have + [r.split(',')[0] for r in reason]



with open('/home/maybe/judiciary/python/IKEA/cpws/pro/reasons', 'r') as f:
    reason = f.readlines()
beijing = [r.strip() for r in reason]

def exists(key, ls):
    return False if True in [True for l in ls if l in key] else True

print(exists('生命权纠纷', have))


rst = []
for b in beijing:
    if exists(b, have):
        rst.append(b)


with open('/home/maybe/judiciary/python/IKEA/cpws/pro/reason_quchong', 'a') as f:
    for r in list(rst):
        f.write(r+'\n')
