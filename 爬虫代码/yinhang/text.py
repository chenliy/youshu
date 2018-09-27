#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/8/3 19:43
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

excle_1 = pd.read_excel(r'C:\Users\ll\Desktop\yijie\2015.xls')

# print(excle_1.index)
# print(type(excle_1.index))
# print(len(excle_1.index))
for x in excle_1.index:
    print(excle_1.loc[x])
# print(excle_1.columns)
#
# print(excle_1['Unnamed: 14'])