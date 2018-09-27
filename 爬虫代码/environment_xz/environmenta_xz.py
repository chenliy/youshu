from pyquery import PyQuery as pq
import requests
import re


url = 'http://www.xzep.gov.cn/index.php/cms/item-view-id-10207.shtml'

headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Cookie':'Wlwz3243235643243455423443355667_P8SESSION=d61cb4878be3b4ac',
    'Host':'www.xzep.gov.cn',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
}

html = requests.get(url=url,headers=headers).text
#print(html)
p = pq(html)
html3 = requests.get(url='http://www.xzep.gov.cn/index.php/cms/item-list-category-1366-page-2.shtml',headers=headers).text
print(re.compile(r'666;">(.*?)&nbsp;来源',re.S).findall(html)[0])
result = p('div.conTxt a')
next = re.compile('(http://www.xzep.gov.cn/index.php/cms/item-list-category-1366-page-\d.shtml)">下一页',re.S).findall(html3)
print(next)
for x in result.items():
    print(x.attr['href'])

url2 = 'http://www.zhb.gov.cn/gkml/sthjbgw/qt/201805/t20180513_439344.htm'
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Cookie':'Wlwz3243235643243455423443355667_P8SESSION=d61cb4878be3b4ac',
    'Host':'www.xzep.gov.cn',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
}

html1 = requests.get(url=url2,headers=headers).text
p = pq(html1)

result2 = p('div.headInfo > *')
for x in result2.items():
    print(x.text())
    print(type(x.text()))
