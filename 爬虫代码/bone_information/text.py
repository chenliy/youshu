import requests
url ='http://www.baidu.com'
print(requests.get(url).cookies.get_dict())
print(requests.get(url).headers)