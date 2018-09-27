#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/16 15:13
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

from yundama import YDMHttp
import requests
from PIL import Image
import io
import re

username = 'yscredit'
password = 'ys@123456'
appid = '4934'
appkey = 'b7132447f5d2b263a61cd4252fd01d6a'

# with open(r'C:\Users\ll\Desktop\02.jpg','rb') as f:
#     a = f.read()
# yundama = YDMHttp(username, password, appid, appkey)
# cid, vcode = yundama.decode_mem(a, '5006', 10)
# print(vcode)
# image = Image.open(io.BytesIO(a))
# image.show()

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'aisino-wsbs-session=de016770-5a45-406e-a5c5-53c74f6503a2',
    'Host': 'etax.ah-n-tax.gov.cn',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
}

#主页url
url = 'http://etax.ah-n-tax.gov.cn/nsr/wzdk/checkybnsrrd'

#验证码url
url2 = 'http://etax.ah-n-tax.gov.cn/nsr/validate?randomNum=654.2100508709448'
imag = requests.get(url2,headers=headers).content

yundama = YDMHttp(username, password, appid, appkey)
cid, vcode = yundama.decode_mem(imag, '5006', 10)
print(vcode)
image = Image.open(io.BytesIO(imag))
image.show()

#查询post

url3 = 'http://etax.ah-n-tax.gov.cn/nsr/wzdk/checkybnsrrd'
data = {
    'nsrsbh':'9134030078306486X3', #信用代码
    'vcode':vcode,#验证码
}
result =  requests.post(url3,headers=headers,data=data).text
print(result)