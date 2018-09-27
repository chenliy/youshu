#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/6 15:08
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome()#第一步声明浏览器对象，这里声明了时chrome对象
#browser = webdriver.Firefox()
#browser = webdriver.Edge()
#browser = webdriver.PhantomJS()
#browser = webdriver.Safari()

try:
    browser.get('https://www.baidu.com')#第二步，利用get 方法来请求网页，传入url

    #查找节点，

    ##查找单个节点，如果网页中有多个，则只返回一个，如果要查找多个elements多个s，返回一个列表，每个元素都是WebElement类型
    inputs = browser.find_element_by_id('kw')#根据id值来查找
    #browser.find_element_by_name()根据name值来查找
    #还可以通过xpath和Css
    #browser.find_element_by_xpath()
    #browser.find_element_by_css_selector()

    #还可以使用通用的方法
    #browser.find_element(By.ID方法,'q'值)


    #节点交互，让浏览器模拟执行一些操作，这些都是针对某一个节点来的

    #输入文字用send_keys()方法
    #清空文字用clear()方法
    #点击按钮用click()方法

    inputs.send_keys('Python')
    inputs.send_keys(Keys.ENTER)
    wait = WebDriverWait(browser,10)
    wait.until(EC.presence_of_all_elements_located((By.ID,'content_left')))
    print(browser.current_url,1)

    #对cookies的操作：7
    print(browser.get_cookies(),2)
    print(browser.page_source,3)#打印源码
except:
    print(4)
    pass
finally:
    browser.close()

#运行代码后，会自动弹出一个Chrome浏览器，浏览器会首先跳转到百度，然后在搜索框中输入python，接着跳转到搜索网页