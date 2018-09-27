# -*- encoding: utf-8 -*-
# Project: dama_test
# Created on 2018/5/22 23:23


from yzm import DamaAPI
import requests
from PIL import Image
import io
import re


headers1 = {
'Accept':'image/webp,image/apng,image/*,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
#'Cookie': 'JSESSIONID=4uQ0gJm0nRRGOoxj4W8JMJaS_2ZBoT0mzOvTHRzk2-V9LYhhSniT!-912624801',
'Host': 'credit.customs.gov.cn',
'Referer': 'http://credit.customs.gov.cn/ccppCopAction/queryCopIn.action',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36',
}
#首页url
base_url = 'http://credit.customs.gov.cn/'
resp = requests.get(base_url,headers=headers1)
cookie = resp.cookies.get_dict()
print(cookie)
sf = re.findall(r'type="hidden" value="(.*?)"',resp.text)[0]
print(sf)


url1 = 'http://credit.customs.gov.cn/ccppCopAction/createImage.action'

resp1 = requests.get(url1,headers=headers1,cookies=cookie)

dma =DamaAPI(vctype='cpws_num')
vcode = dma.yundamaByCode(resp1.content,codetype='5006')
print(vcode)
image = Image.open(io.BytesIO(resp1.content))
image.show()


headers2 = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
'Content-Type': 'application/x-www-form-urlencoded',
#'Cookie': 'JSESSIONID=4uQ0gJm0nRRGOoxj4W8JMJaS_2ZBoT0mzOvTHRzk2-V9LYhhSniT!-912624801',
'Origin': 'http://credit.customs.gov.cn',
'Host': 'credit.customs.gov.cn',
'Upgrade-Insecure-Requests': '1',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Referer': 'http://credit.customs.gov.cn/',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36',
}
data = 'copName=%E5%BF%AB%E9%92%B1%E6%94%AF%E4%BB%98%E6%B8%85%E7%AE%97%E4%BF%A1%E6%81%AF%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&sf={}&x=58&y=14&randomCode={}'.format(sf,vcode)

resp2 = requests.post(url='http://credit.customs.gov.cn/ccppCopAction/queryCopIn.action',headers=headers2,data=data,cookies=cookie)
print(resp2.text)
#
