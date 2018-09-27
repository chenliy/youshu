#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/6 19:13
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

import time
from selenium import webdriver

browser = webdriver.Chrome()
browser.get(('https://www.baidu.com'))
browser.execute_script('window.open()')#这个JavaScript语句新开启一个选项卡
print(browser.window_handles)#当前开启的所有选项卡

browser.switch_to_window(browser.window_handles[1])#切换到第二个选项卡
browser.get('https://www.taobao.com')

time.sleep(1)

browser.switch_to_window(browser.window_handles[0])#切换到第一个选项卡
browser.get('https://python.org')