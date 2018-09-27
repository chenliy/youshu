#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/7 9:10
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

'''
splash是一个JavaScript渲染服务，是一个带有HTTP API 的轻量级浏览器，
同时它对接了Python中的Twisted和QT库。利用他我们同样可以实现动态渲染页面的抓取

我们可以实现：

1.异步方式处理多个网页渲染过程
2.获取渲染后的页面的源代码或截图
3.通过关闭图片渲染或者使用Adblock规则来加快页面渲染速度
4.可执行特定的JavaScript脚本
5.可以通过Lua脚本来控制页面渲染过程
6.获取渲染的详细过程并通过 HAR (HTTP Archive）格式呈现

'''

try:
    pass
except:
