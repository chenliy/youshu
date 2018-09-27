#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/8/1 10:59
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

import pandas as pd
from math import isnan
# import requests
# import xlrd
# import xlwt
#
# url = 'http://www.qzzjfy.gov.cn/wp-content/uploads/2018/07/2018-07-1775.xls'
# headers = {
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#             'Accept-Encoding': 'gzip, deflate',
#             'Accept-Language': 'zh-CN,zh;q=0.9',
#             'Cache-Control': 'max-age=0',
#             'Connection': 'keep-alive',
#             'Cookie': 'PHPSESSID=tn2icp67jusg3mcgh63ojb29u7; __jsluid=c2ff96e740714f3f56276887195602c5',
#             'Host': 'www.qzzjfy.gov.cn',
#             'Upgrade-Insecure-Requests': '1',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'}
#
# r = requests.get(url,headers=headers).content


data = pd.read_excel(r'C:\Users\ll\Desktop\2.xls',header=None)
print(data.columns)
print(data.index)

#第0行为标题
print(data.iloc[0,0].replace(' ', '').replace('\u3000', '').replace('\xa0', ''))
# for i in range(len(data.index)):
#     for j in range(len(data.columns)):
#         print(data.iloc[i,j])
#第一行，第二行，作为主键
list1 = []
list2 = []
list3 = []
for j in range(len(data.columns)):
    list1.append(data.iloc[1,j])
    list2.append(data.iloc[2,j])
    list3.append(data.iloc[3,j])



for i in range(len(list2)):
    print(list2[i])
    try:
        if isnan(list2[i]):
            print(1)
            list2[i] = list1[i]
    except:
        pass

def get_content(title,result):
    if len(title) == len(result):
        content = {}
        for i in range(len(title)):
            content[title[i]] = result[i]
        return content
    else:
        print('形式有错误')
        return


print(get_content(list2,list3))