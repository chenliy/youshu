#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/8/6 18:41
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

import pandas as pd
url = 'http://fjlyzy.chinacourt.org/article/detail/2018/08/id/3444165.shtml'
dataframes = pd.read_html(io=url)
for dataframe in dataframes:
    print(type(dataframe))
    print(dataframe)
    writer = pd.ExcelWriter(r'C:\Users\ll\Desktop\output.xlsx')
    dataframe.to_excel(writer, 'Sheet1')
    writer.save()
