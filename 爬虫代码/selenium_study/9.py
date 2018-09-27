#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/6 19:20
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException

browser = webdriver.Chrome()

try:
    browser.get('https://www.baidu.com')
except TimeoutException:
    print('Time Out')

try:
    browser.find_element_by_id('hello')
except NoSuchElementException:
    print('No Element')
finally:
    browser.close()