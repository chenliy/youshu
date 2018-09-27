#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/6 19:04
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

#前进后退
import time
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.baidu.com')
browser.get('https://www.taobao.com')
browser.get('https://www,python.org')

browser.back()#后退
time.sleep(1)
browser.forward()#前进
browser.close()