#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/31 9:10
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

# url = 'http://kmzy.ynfy.gov.cn/u/cms/www/201712/19104933vvut.doc'
# import requests
#
# r = requests.get(url).content
# with
# print(r)
# with open(r'C:\Users\ll\Desktop\123.docx','wb',encoding='utf-8') as f:
#     f.write(r)


import subprocess
import os
import requests

def download_parse(filename,content):


    #url = 'http://ssfw.gzcourt.gov.cn:8080/webapp/area/gz/cpws/cpws_view.jsp?lsh=255100000001436&xh=0000'
    try:


        with open(filename,'wb') as f:
            f.write(content)
        output = subprocess.check_output(["antiword", filename])
        text  =  output.decode('utf-8')
        return text
    except Exception as e:
        print(e)
    finally:
        os.remove(filename)

url = 'http://kmzy.ynfy.gov.cn/u/cms/www/201712/19104933vvut.doc'
file_name = url.split('/')[-1]
response = requests.get(url)

text = download_parse(filename=file_name,content=response.content)
print(text)

