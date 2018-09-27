# -*- encoding: utf-8 -*-
# Project: damaServer
# Created on 2018/5/22 20:39

import base64,json,requests
from io import BytesIO

#Base64是一种用64个字符来表示任意二进制数据的方法

class DamaAPI(object):


    # __resUrl = 'http://10.1.5.159:7475/captcha/vcode'
    # __yundamaUrl = 'http://10.1.5.159:7475/captcha/feecrack/vcode'

    __resUrl = 'http://10.10.50.5:7475/captcha/vcode'
    __yundamaUrl = 'http://10.10.50.5:7475/captcha/feecrack/vcode'
          __ocrUrl = 'http://10.10.50.5:7475/captcha/ocrcrack/vcode'

    #__ocrUrl = 'http://localhost:7475/captcha/ocrcrack/vcode'

    def __init__(self,vctype='cpws_num'):

        self._headers= {
            'Accept':'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        }
        self._vctype = vctype


    def imageByCode(self,imageData):
        '''
        :param imageData: 图片数据
        :return: 返回验证码
        '''
        url = self.__resUrl
        imgdata = {'vctype':self._vctype, 'imgdata':str(base64.encodebytes(imageData), 'ascii')}
        resp = requests.post(url, data=imgdata,timeout=10)
        json_vcode = json.loads(resp.text)
        #print(resp.text)
        # json --> {'vcode': '83962 ', 'accuracy': '1.0'}
        vcode = json_vcode['vcode'].strip()
        return vcode



    def urlByCode(self,url,**kwargs):
        '''
        :param url: 验证码url
        :param kwargs: 请求url参数，例：proxy，params等
        :return:
        '''
        response = requests.get(url,headers=self._headers,**kwargs)
        return self.imageByCode(response.content)


    def yundamaByCode(self,imageData,codetype='1005'):

        '''
        :param imageData: 图片数据
        :param codetype: 验证码类型码
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
        :return:
        '''

        imgdata = {'vctype':'yundama','imgdata':str(base64.encodebytes(imageData),'ascii'),'codetype':codetype}
        resp = requests.post(self.__yundamaUrl, data=imgdata,timeout=10)
        json_vcode = json.loads(resp.text)
        # json --> {'vcode': '83962 ', 'accuracy': '1.0'}
        vcode = json_vcode['vcode'].strip()
        return vcode

    def yundamaUrlByCode(self,url,codetype='1005',**kwargs):
        '''

        :param url: 验证码url
        :param kwargs: 请求url参数，例：proxy，params等
        :return:
        '''
        response = requests.get(url,headers=self._headers,**kwargs)
        return self.yundamaByCode(response.content,codetype=codetype)

    def ocrByCode(self,imageData,**kwargs):

        '''
        :param imageData:
        :param kwargs: cthrs and lthrs
        :return:
        '''
        imgdata = {'imgdata':str(base64.encodebytes(imageData), 'ascii'),'cthrs':kwargs.get('cthrs'),'lthrs':kwargs.get('lthrs')}
        resp = requests.post(self.__ocrUrl, data=imgdata)
        json_vcode = json.loads(resp.text)
        # json --> {'vcode': '83962 ', 'accuracy': '1.0'}
        vcode = json_vcode['vcode'].strip()
        return vcode


    def ocrUrlByCode(self,url,**kwargs):

        response = requests.get(url,headers=self._headers)
        return self.ocrByCode(response.content,kwargs=kwargs)


    def pixImage(self,img,w=0,d=0):
        if not w:
            w = 70
        if not d:
            d = 136

        pixdata = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][0] < w:
                    pixdata[x, y] = (0, 0, 0, 255)

        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][1] < d:
                    pixdata[x, y] = (0, 0, 0, 255)

        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][2] > 0:
                    pixdata[x, y] = (255, 255, 255, 255)

        return img

    def test_ocr(self,imageData,w=0,d=0):

        from PIL import Image
        try:
            from pytesseract import image_to_string
        except:
            from pytesseract.pytesseract import image_to_string

        if isinstance(imageData,bytes):
            img = Image.open(BytesIO(imageData))
            img = self.pixImage(img,w=w,d=d)
            return image_to_string(img)
        else:
            raise Exception('imageData not <class bytes> --You should give me a bytes type of data ')

if __name__ == '__main__':

    # url = 'http://www.bidchance.com/common/img.jsp?n=l&0.32668580370058664'
    # response = requests.get(url)
    # print(response.text)
    with open(r'C:\Users\ll\Desktop\123.jpg','rb') as f:
        data = f.read()
        print(data)

    from PIL import Image
    image = Image.open(r'C:\Users\ll\Desktop\123.jpg')
    image.show()
    dama = DamaAPI()
    vcode = dama.ocrByCode(data,cthrs=180,lthrs=0)
    print(vcode)