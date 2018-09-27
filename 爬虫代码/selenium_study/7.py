#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/6 19:08
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com
from selenium import webdriver
browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/explore')
print(browser.get_cookies())

browser.add_cookie({'name':'name','domain':'www.zhihu.com','value':'germey'})
print(browser.get_cookies())

browser.delete_all_cookies()
print(browser.get_cookies())