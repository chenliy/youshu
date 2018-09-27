#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/6 17:32
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

#延时等待
#在selenium中，get()方法会在网页框架加载结束后结束执行，此时如果获取page-source，可能并不是浏览器完全加载完成的页面
#如果某些页面有额外的Ajax请求，我们在网页源代码中也不一定能获取的到，所以这里需要延时等待一段时间，确保节点已经加载出来了

from selenium import webdriver
#隐式等待
#如果selenium没有在DOM中找到节点，将继续等待，等一会再找，超过设定时间后，则抛出找不到节点的异常，默认时间是0
browser = webdriver.Chrome()
browser.implicitly_wait(10)#隐式等待10秒
browser.get('https://www.zhihu.com/explore')
inputs = browser.find_element_by_class_name('zu-top-add-question')
print(inputs)
browser.close()
#显式等待
#指定要查找的节点，然后指定一个最长的等待时间，如果在规定时间内加载出了这个节点，就返回查找的节点，没有就异常

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
browser.get('https://www.taobao.com/')
wait = WebDriverWait(browser,10)
inputs = wait.until(EC.presence_of_all_elements_located((By.ID,'q')))
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.btn-search')))
print(inputs,button)

#关于等待条件，还有很多，比如判断标题内容，判断某个节点是否出现了某文字等。p259表格