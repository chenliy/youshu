#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018/8/2 9:26
# Project: 
# @Author: ZQJ
# @Email : zihe@yscredit.com

import requests
import random

#post url
url = 'https://rmfygg.court.gov.cn/web/rmfyportal/noticeinfo?p_p_id=noticelist_WAR_rmfynoticeListportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=initNoticeList&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1#1'


# data = {'_noticelist_WAR_rmfynoticeListportlet_content': '',
#             '_noticelist_WAR_rmfynoticeListportlet_searchContent': '',
#             '_noticelist_WAR_rmfynoticeListportlet_IEVersion': 'ie',
#             '_noticelist_WAR_rmfynoticeListportlet_flag': 'init',
#             '_noticelist_WAR_rmfynoticeListportlet_noticeType':'',
#             '_noticelist_WAR_rmfynoticeListportlet_aoData': '[{"name":"sEcho","value":5},{"name":"iColumns","value":6},{"name":"sColumns","value":",,,,,"},{"name":"iDisplayStart","value":0},{"name":"iDisplayLength","value":10},{"name":"mDataProp_0","value":null},{"name":"mDataProp_1","value":null},{"name":"mDataProp_2","value":null},{"name":"mDataProp_3","value":null},{"name":"mDataProp_4","value":null},{"name":"mDataProp_5","value":null}]'
#                }

data = {
    '_noticelist_WAR_rmfynoticeListportlet_content':'',
    '_noticelist_WAR_rmfynoticeListportlet_searchContent': '',
    '_noticelist_WAR_rmfynoticeListportlet_courtParam': '',
    '_noticelist_WAR_rmfynoticeListportlet_IEVersion': 'ie',
    '_noticelist_WAR_rmfynoticeListportlet_flag': 'init',
    '_noticelist_WAR_rmfynoticeListportlet_noticeType': '',
    '_noticelist_WAR_rmfynoticeListportlet_noticeTypeVal': '全部',
    '_noticelist_WAR_rmfynoticeListportlet_aoData': '[{"name":"sEcho","value":8},{"name":"iColumns","value":6},{"name":"sColumns","value":",,,,,"},{"name":"iDisplayStart","value":0},{"name":"iDisplayLength","value":15},{"name":"mDataProp_0","value":null},{"name":"mDataProp_1","value":null},{"name":"mDataProp_2","value":null},{"name":"mDataProp_3","value":null},{"name":"mDataProp_4","value":null},{"name":"mDataProp_5","value":null}]',
}
UA = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        ]
header = {
        'accept':'application/json,text/javascript,*/*;q=0.01',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'UM_distinctid=164f83c06cf573-01a5eb5d1f013f-47e1e39-1fa400-164f83c06d0341; JSESSIONID=F4334FBD95B533028CF19F15562DC7E3; LFR_SESSION_STATE_20158=1533173510492; tgw_l7_route=fb4686ab27ce2dbeb7cbdd7edefce9f4; CNZZDATA1273632440=2002546711-1531699364-https%253A%252F%252Fwww.baidu.com%252F%7C1533173527',
        'origin':'http://rmfygg.court.gov.cn',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'x-requested-with':'XMLHttpRequest',
        'User-Agent':random.choice(UA),
        }

html = requests.post(url,headers=header,data=data).text
r = requests.post(url,headers=header,data=data)
print(r.status_code)
print(html)

#第一页
'_noticelist_WAR_rmfynoticeListportlet_aoData: [{"name":"sEcho","value":16},{"name":"iColumns","value":6},{"name":"sColumns","value":",,,,,"},{"name":"iDisplayStart","value":0},{"name":"iDisplayLength","value":15},{"name":"mDataProp_0","value":null},{"name":"mDataProp_1","value":null},{"name":"mDataProp_2","value":null},{"name":"mDataProp_3","value":null},{"name":"mDataProp_4","value":null},{"name":"mDataProp_5","value":null}]'

#第二页
'_noticelist_WAR_rmfynoticeListportlet_aoData: [{"name":"sEcho","value":17},{"name":"iColumns","value":6},{"name":"sColumns","value":",,,,,"},{"name":"iDisplayStart","value":15},{"name":"iDisplayLength","value":15},{"name":"mDataProp_0","value":null},{"name":"mDataProp_1","value":null},{"name":"mDataProp_2","value":null},{"name":"mDataProp_3","value":null},{"name":"mDataProp_4","value":null},{"name":"mDataProp_5","value":null}]'

#第三页
'_noticelist_WAR_rmfynoticeListportlet_aoData: [{"name":"sEcho","value":18},{"name":"iColumns","value":6},{"name":"sColumns","value":",,,,,"},{"name":"iDisplayStart","value":30},{"name":"iDisplayLength","value":15},{"name":"mDataProp_0","value":null},{"name":"mDataProp_1","value":null},{"name":"mDataProp_2","value":null},{"name":"mDataProp_3","value":null},{"name":"mDataProp_4","value":null},{"name":"mDataProp_5","value":null}]'

#第四页
'_noticelist_WAR_rmfynoticeListportlet_aoData: [{"name":"sEcho","value":19},{"name":"iColumns","value":6},{"name":"sColumns","value":",,,,,"},{"name":"iDisplayStart","value":45},{"name":"iDisplayLength","value":15},{"name":"mDataProp_0","value":null},{"name":"mDataProp_1","value":null},{"name":"mDataProp_2","value":null},{"name":"mDataProp_3","value":null},{"name":"mDataProp_4","value":null},{"name":"mDataProp_5","value":null}]'



data = {'_noticelist_WAR_rmfynoticeListportlet_content': '',
                '_noticelist_WAR_rmfynoticeListportlet_searchContent': '',
                '_noticelist_WAR_rmfynoticeListportlet_IEVersion': 'ie',
                '_noticelist_WAR_rmfynoticeListportlet_flag': 'init',
                '_noticelist_WAR_rmfynoticeListportlet_noticeType':'',
                '_noticelist_WAR_rmfynoticeListportlet_aoData': '[{"name":"sEcho","value":%s},{"name":"iColumns","value":6},{"name":"sColumns","value":",,,,,"},{"name":"iDisplayStart","value":%s},{"name":"iDisplayLength","value":15},{"name":"mDataProp_0","value":null},{"name":"mDataProp_1","value":null},{"name":"mDataProp_2","value":null},{"name":"mDataProp_3","value":null},{"name":"mDataProp_4","value":null},{"name":"mDataProp_5","value":null}]'%(1,2)
                   }
print(data)









