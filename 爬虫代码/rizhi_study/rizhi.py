#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/7/5 16:01
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

import logging
import sys

#获取logger实例，如果参数为空，则返回root Logger
logger = logging.getLogger('zqj')

#指定Logger输出格式
formatter = logging.Formatter('%(asctime)s %(levelname)-8s:%(message)s')

#文件日志
file_handler = logging.FileHandler('')