import http.client, mimetypes, urllib, json, time, requests

######################################################################

# code type: xx = 00 ~ 20, 00 表示不定长
#    10xx    xx位英文, 数字
#    20xx    xx位纯汉字
#    30xx    xx位纯英文
#    40xx    xx位纯数字
#    5000    不定长汉字英文数字、符号、空格
#    5001    不定长汉字英文数字、符号、空格（区分大小写）
#    5006    6位英文数字符号
#    6100    google验证码（只输入斜体部分）
#    6200    九宫格坐标验证码（9个汉字选出4个）
#    6201    九宫格坐标验证码（9个汉字选出1-4个）
#    6300    加减乘除计算题
#    6301    知识问答计算题（结果为数字）
#    6400    4组汉字4选1
#    6500    选出两个相同动物序号
#    6600    单选题根据问题选择答案编号
#    6601    单选题选出字符所在位置
#    6602    单选题有多少个指定的汉字
#    6701    多选题返回数字（8个图中选择1-8个）
#    6101    简单问答题（拼音字母、汉字、计数、认图）
#    4105    模糊动态5位数字

######################################################################

class YDMHttp:

    apiurl = 'http://api.yundama.com/api.php'
    username = ''
    password = ''
    appid = ''
    appkey = ''

    def __init__(self, username, password, appid, appkey):
        self.username = username  
        self.password = password
        self.appid = str(appid)
        self.appkey = appkey

    def request(self, fields, files=[]):
        response = self.post_url(self.apiurl, fields, files)
        response = json.loads(response)
        return response
    
    def balance(self):
        data = {'method': 'balance', 'username': self.username, 'password': self.password, 'appid': self.appid, 'appkey': self.appkey}
        response = self.request(data)
        if (response):
            if (response['ret'] and response['ret'] < 0):
                return response['ret']
            else:
                return response['balance']
        else:
            return -9001
    
    def login(self):
        data = {'method': 'login', 'username': self.username, 'password': self.password, 'appid': self.appid, 'appkey': self.appkey}
        response = self.request(data)
        if (response):
            if (response['ret'] and response['ret'] < 0):
                return response['ret']
            else:
                return response['uid']
        else:
            return -9001

    def upload(self, filename, codetype, timeout):
        data = {'method': 'upload', 'username': self.username, 'password': self.password, 'appid': self.appid, 'appkey': self.appkey, 'codetype': str(codetype), 'timeout': str(timeout)}
        file = {'file': filename}
        response = self.request(data, file)
        if (response):
            if (response['ret'] and response['ret'] < 0):
                return response['ret']
            else:
                return response['cid']
        else:
            return -9001

    def result(self, cid):
        data = {'method': 'result', 'username': self.username, 'password': self.password, 'appid': self.appid, 'appkey': self.appkey, 'cid': str(cid)}
        response = self.request(data)
        return response and response['text'] or ''

    def decode(self, filename, codetype, timeout):
        cid = self.upload(filename, codetype, timeout)
        if (cid > 0):
            for i in range(0, timeout):
                result = self.result(cid)
                if (result != ''):
                    return cid, result
                else:
                    time.sleep(1)
            return -3003, ''
        else:
            return cid, ''

    def report(self, cid):
        data = {'method': 'report', 'username': self.username, 'password': self.password, 'appid': self.appid, 'appkey': self.appkey, 'cid': str(cid), 'flag': '0'}
        response = self.request(data)
        if (response):
            return response['ret']
        else:
            return -9001

    def post_url(self, url, fields, files=[]):
        for key in files:
            files[key] = open(files[key], 'rb');
        res = requests.post(url, files=files, data=fields)
        return res.text

    def decode_mem(self, imgfile, codetype, resultTimeout):
        cid = -9001
        fields = {'method': 'upload', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey, 'codetype': str(codetype), 'timeout': str(resultTimeout)}
        try:
            # 这步只是上传打码图片
            response = requests.post(self.apiurl, files={'file': imgfile}, data=fields, timeout=20)
            if response.ok:
                ret = json.loads(response.text)
                if (ret['ret'] and ret['ret'] < 0):
                    cid =  ret['ret']
                else:
                    cid = ret['cid']

        except Exception as e:
            print('decode_mem', e)

        if (cid > 0):
            for i in range(0, resultTimeout*2):
                # 结果需自己再次请求，不是打码后自动返回
                result = self.result(cid)
                if (result != ''):
                    return cid, result
                else:
                    time.sleep(0.5)
            return -3003, ''
        else:
            return cid, ''

######################################################################

# # 用户名
# username    = 'username'

# # 密码
# password    = 'password'                            

# # 软件ＩＤ，开发者分成必要参数。登录开发者后台【我的软件】获得！
# appid       = 1                                     

# # 软件密钥，开发者分成必要参数。登录开发者后台【我的软件】获得！
# appkey      = '22cc5376925e9387a23cf797cb9ba745'    

# # 图片文件
# filename    = 'getimage.jpg'                        

# # 验证码类型，# 例：1004表示4位字母数字，不同类型收费不同。请准确填写，否则影响识别率。在此查询所有类型 http://www.yundama.com/price.html
# codetype    = 1004

# # 超时时间，秒
# timeout     = 60                                    

# # 检查
# if (username == 'username'):
#     print('请设置好相关参数再测试')
# else:
#     # 初始化
#     yundama = YDMHttp(username, password, appid, appkey)

#     # 登陆云打码
#     uid = yundama.login();
#     print('uid: %s' % uid)

#     # 查询余额
#     balance = yundama.balance();
#     print('balance: %s' % balance)

#     # 开始识别，图片路径，验证码类型ID，超时时间（秒），识别结果
#     cid, result = yundama.decode(filename, codetype, timeout);
#     print('cid: %s, result: %s' % (cid, result))

######################################################################
