#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/8/6 9:47
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

import requests
from bs4 import BeautifulSoup
headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'fjlyzy.chinacourt.org',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
}

url = 'http://fjlyzy.chinacourt.org/article/detail/2015/01/id/2037182.shtml'

response = requests.get(url,headers=headers)
#print(response.status_code)
html = response.text

soup = BeautifulSoup(html,'lxml')

trs = soup.find_all('tr')

createVar = locals()
result_total = []
try:
    length_list = []
    for i,tr in enumerate(trs):
        createVar['tr' + str(i)] = []
        tds = tr.find_all('td')
        for j,td in enumerate(tds):
            #利用创建的变量，列表，append当前tr里面的每一个td 字典

            createVar['td' + str(j)] = {}
            exec('td{}[{}] = {}'.format(j,'"v"','"{}"'.format(td.text)))
            exec('td{}[{}] = {}'.format(j, '"s"', '"{}"'.format(td.attrs['style'])))
            exec('tr{}.append({})'.format(i,eval('td{}'.format(j))))
        result_total.append(eval('tr{}'.format(i)))
        length_list.append(len(eval('tr{}'.format(i))))

    #print(result_total)
    #到这里创建了各个tr标签，这是一个列表，内容是各个td标签，是字典
    #通过长度来判断，当前tr是否为title
    #length_list 记录了各个tr标签的长度


    length_dict = {}
    for eachs in result_total:
        for each in eachs:
            key = each.get('s','')
            if key not in length_dict.keys():
                exec('length_dict[{}] = {}'.format('"{}"'.format(key),1))
            else:
                exec('length_dict[{}] = {}'.format('"{}"'.format(key),length_dict.get(key) + 1))

    #length_dict 把每个style出现的次数构成了一个字典
    #print(length_dict)



    #如果已经出现某一行的长度大于3，那么也就是说内容已经出现过了，后面的内容可能向上也可能向下关联
    for i in range(len(length_list)):
        if length_list[i] > 3:
            #print(length_list[i])
            first_content_num = i
            #print(first_content_num)
            break
        if i  == len(length_list)-1:
            first_content_num = 2


    title = []
    #将之前所有行都纳入title中，最后一个需要判断一下是不是向下关联:
    for i in range(first_content_num):
        for j in range(len(eval('tr{}'.format(i)))):
            title.append(eval('tr{}'.format(i))[j].get('v',''))

    #print(title)
    index_list = []
    for x in eval('tr{}'.format(first_content_num)):
        index_list.append(x.get('v',''))

    if len(eval('tr{}'.format(first_content_num + 1))) < 3:
        first_content_num = first_content_num + 1
        for x in eval('tr{}'.format(first_content_num)):
            index_list.append(x.get('v', ''))

    #print(index_list)
    index_list_findall = []
    if '终判时间' in index_list and '入监时间' in index_list:
        for x in index_list:
            if x == '入监时间':
                pass
            elif x == '终判时间':
                x = '终判时间' + 'and入监时间'
                index_list_findall.append(x)
            else:
                index_list_findall.append(x)
    #print(index_list_findall)

    content_total = []
    for i in range(first_content_num + 1,len(trs)):
        content_list = []
        for each in eval('tr{}'.format(i)):
            content_list.append(each.get('v',''))
        content_total.append(content_list)
    for i in range(0,len(content_total),2):
        content_total[i][4]  = content_total[i][4]+ 'to' + content_total[i+1][0]
        content_total[i][5] = content_total[i][5]+ 'to' + content_total[i+1][1]
        content_total[i][6] = content_total[i][6] + 'to' + content_total[i + 1][2]

    content_total_findall = []
    for x in content_total:
        if len(x) > 5:
            content_total_findall.append(x)
    #print(content_total_findall)
    for x in content_total_findall:
        result = {}
        result['标题'] = str(title)
        if len(x) == len(index_list_findall):
            for i in range(len(index_list_findall)):
                result[index_list_findall[i]] = x[i]
        #print(result)

except Exception as e:
    print(e)
    print("{}该网页形式有异".format(response.url))