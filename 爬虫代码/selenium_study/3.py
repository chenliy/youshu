#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/6 16:57
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

#执行JavaScript，对于某些操作，Selenium API 并没有提供，比如下拉进度条，他可以直接模拟运行JavaScript

from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/explore')
browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
browser.execute_script('alert("To Bottom")')
