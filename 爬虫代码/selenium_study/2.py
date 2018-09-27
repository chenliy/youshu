#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/6 16:11
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

from selenium import webdriver
from selenium.webdriver import ActionChains

browser = webdriver.Chrome()
url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'

browser.get(url)
browser.switch_to.frame('iframeResult')
#依次选中需要拖拽的节点和拖拽到目标的结果
source = browser.find_element_by_css_selector('#draggable')
target = browser.find_element_by_css_selector('#droppable')
#声明ActionChains对象并将他赋值给actions
actions = ActionChains(browser)
#通过调用drag_and_drop方法
actions.drag_and_drop(source,target)
#再调用perform执行动作
actions.perform()