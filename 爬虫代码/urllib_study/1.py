import urllib.request

response = urllib.request.urlopen('https://www.python.org')
print(response.read().decode('utf-8'))
print(type(response))
print(response.status)#状态码
print(response.getheaders())#返回响应的头信息，注意这里不是请求头信息
print(response.getheader('Server'))#具体筛选出Server的内容

#urllib.request.urlopen(url=,data=,timeout=,cafile=,capath=,cadefault=,context=)

#有了data参数在，那就是post请求，要用bytes()转换

import urllib.parse

data = bytes(urllib.parse.urlencode({'word':'hell0'}),encoding='utf-8')
response = urllib.request.urlopen('http://httpbin.org/post',data=data)
print(response.read())

#timeout 超时时间

import socket
import urllib.error
try:
    response = urllib.request.urlopen('http://httpbin.org/get',timeout=0.1)
except urllib.error.URLError as e:
    print(e.reason)
    if isinstance(e.reason,socket.timeout):
        print('Time Out')

#如果需要在请求头中加入Headers等信息，就要利用Request类来使用
url = 'http://httpbin.org/post'

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
    'Host':'httpbin.org'
}
dict = {
    'name':'zqj'
}
data = bytes(urllib.parse.urlencode(dict),encoding='utf-8')
req = urllib.request.Request(url=url,data=data,headers=headers,method='POSt')
response = urllib.request.urlopen(req)
print(response.read().decode('utf-8'))

#利用Handler来构建Opener

from urllib.request import HTTPPasswordMgrWithDefaultRealm,HTTPBasicAuthHandler,build_opener
from urllib.error import URLError
username = 'yscredit'
passwoed = 'youshu808'
url = 'http://www.bidchance.com/logon.do'

#验证账号密码,首先实例化HTTPBasicAuthHandler对象，他的参数是HTTPPasswordMgrWithDefaultRealm对象
#然后利用他的add_password,添加用户名和密码,这样就建立了一个处理验证的handler
#接着利用这个handler和build_opener构建一个opener
#最后利用这个opener打开
p = HTTPPasswordMgrWithDefaultRealm()
p.add_password(None,url,user=username,passwd=passwoed)
auth_handler = HTTPBasicAuthHandler(p)
opener = build_opener(auth_handler)
try:
    result = opener.open(url)
    html = result.read().decode('utf-8')
    print(html)
except URLError as e:
    print(e.reason)


