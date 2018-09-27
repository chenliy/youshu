from IKEA.shixin.process.base_process import Base
import json
from pyquery import PyQuery as pq
from lxml import etree
from bs4 import BeautifulSoup
import re
from datetime import datetime

class YunNan(Base):
    def __init__(self,**kwargs):
        super(YunNan,self).__init__(**kwargs)
        
        self.soup = BeautifulSoup(self.detail, 'lxml')

        self.is_div = self.soup.find('div', {'class': 'sswy_article_m'}).findAll('div')
        if not self.is_div:
            self.detail_results = self.soup.find('div', {'class': 'sswy_article_m'}).findAll('tr')[-1].findAll('td')
            self.case_code = self.detail_results[0].get_text() if self.detail_results[0] else ''
            self.name = self.detail_results[1].get_text() if self.detail_results[1] else ''
            self.card_num = self.detail_results[2].get_text() if self.detail_results[2] else ''
            self.gist_id = self.detail_results[3].get_text() if self.detail_results[3] else ''
            self.performance = self.detail_results[5].get_text() if self.detail_results[5] else ''
            self.disrupt_type_name = self.detail_results[6].get_text() if self.detail_results[6] else ''
            self.business_entity = ''
            self.reg_date = ''
            self.court_name = ''
            self.gist_unit = ''
            self.duty = ''
            self.sex = ''
            self.age = ''
        else:
            self.detail_results = self.soup.find('div', {'class': 'sswy_article_m'}).get_text().replace('\n\n\n',
                                                                                                        '').replace(
                '\n\n', ';').replace('\n',';')
            # print(self.detail_results)
            self.name = re.findall(r'被执行人：(.+?);', self.detail_results)[0] if re.findall(r'被执行人：(.+?);', self.detail_results) else ''
            self.case_code = re.findall(r'案号：(.+?);', self.detail_results)[0] if re.findall(r'案号：(.+?);', self.detail_results) else ''
            self.card_num = re.findall(r'码：(.+?);', self.detail_results)[0] if re.findall(r'码：(.+?);', self.detail_results) else ''
            self.business_entity = re.findall(r'法定代表人或者负责人姓名：(.+?);', self.detail_results)[0] if re.findall(r'法定代表人或者负责人姓名：(.+?);', self.detail_results) else ''
            self.reg_date = re.findall(r'立案时间：(.+?);', self.detail_results)[0].strip() if re.findall(r'立案时间：(.+?);', self.detail_results) else '1900-01-01'
            if '.' in self.reg_date:
                self.reg_date = datetime.strptime(self.reg_date,'%Y.%m.%d')
                self.reg_date = datetime.strftime(self.reg_date,'%Y-%m-%d')
            self.court_name = re.findall(r'执行法院：(.+?);', self.detail_results)[0] if re.findall(r'执行法院：(.+?);', self.detail_results) else ''
            self.gist_id = re.findall(r'文号：(.+?);', self.detail_results)[0] if re.findall(r'文号：(.+?);', self.detail_results) else ''
            self.gist_unit = re.findall(r'单位：(.+?);', self.detail_results)[0] if re.findall(r'单位：(.+?);', self.detail_results) else ''
            self.duty = re.findall(r'义务：(.+?);', self.detail_results)[0] if re.findall(r'义务：(.+?);', self.detail_results) else ''
            self.performance = re.findall(r'履行情况：(.+?);', self.detail_results)[0] if re.findall(r'履行情况：(.+?);', self.detail_results) else ''
            self.disrupt_type_name = re.findall(r'具体情形：(.+?);', self.detail_results)[0] if re.findall(r'具体情形：(.+?);', self.detail_results) else ''
            self.sex = re.findall(r'性别：(.+?);', self.detail_results)[0] if re.findall(r'性别：(.+?);', self.detail_results) else ''
            self.age = re.findall(r'年龄：(.+?);', self.detail_results)[0] if re.findall(r'年龄：(.+?);', self.detail_results) else ''

    def sxbzx(self):
        self.executive_person['name'] = self.name
        self.executive_person['case_code'] = self.case_code
        self.executive_person['business_entity'] = self.business_entity
        self.executive_person['sex'] = self.sex
        self.executive_person['age'] = self.age
        self.executive_person['card_num'] = self.card_num
        self.executive_person['reg_date'] = self.reg_date
        self.executive_person['court_name'] = self.court_name
        self.executive_person['gist_id'] = self.gist_id
        self.executive_person['gist_unit'] = self.gist_unit
        self.executive_person['duty'] = self.duty
        self.executive_person['performance'] = self.performance
        self.executive_person['disrupt_type_name'] = self.disrupt_type_name
        self.executive_person['operator'] = 'wangfeng'
        print(self.executive_person)
        pass


if __name__ == '__main__':
    s = '''
       <li>&#13;
<a href="http://dlyp.ynfy.gov.cn:80/sxbzxr/55708.jhtml" title="失信被执行人杨本华" target="_blank">失信被执行人杨本华</a>&#13;
<div class="date" style="float:right">2017-02-28 14:14:41</div></li>
    '''
    d = '''
        <!DOCTYPE HTML>

<html lang="en-US">

<head>

	<meta charset="UTF-8">

	<title>剑川县人民法院</title>

	<link rel="stylesheet" type="text/css" href="/../r/cms/www/jchfy/css/sswy.css" media="all" />

</head>

<body>

	<div class="sswy_bj">	

		<div class="sub_page_head">

<div class="sswy_top">

	<div class="sswy_tel_box"></div>

	<ul class="sswy_top_nav">



		<li class="load"><a href="http://www.susong51.com/login/pro.htm?fy=3475"><em></em>登录</a></li>	

		<li class="active"><a href="http://www.susong51.com/login/register.htm?fy=3475"><em></em>注册</a></li>



	</ul>

</div>
			<!-- sswy_top end -->

<div class="sswy_main_nav">

	<ul class="sswy_main_nav_inner">

	<li><a href="/..">首&nbsp;&nbsp;&nbsp;&nbsp;页</a></li>

	<li><a href="http://dljc.ynfy.gov.cn:80/fyyw/index.jhtml" >法院要闻</a></li>

	<li><a href="http://dljc.ynfy.gov.cn:80/fygg/index.jhtml" >法院公告</a></li>

	<li><a href="http://wenshu.court.gov.cn/" >裁判文书</a></li>

	<li><a href="http://dljc.ynfy.gov.cn:80/splc/index.jhtml" >审判流程</a></li>

	<li><a href="http://dljc.ynfy.gov.cn:80/zxxx/index.jhtml" >执行信息</a></li>

	<li><a href="http://dljc.ynfy.gov.cn:80/tssp/index.jhtml" >庭审视频</a></li>

	<li><a href="http://dljc.ynfy.gov.cn:80/zdxal/index.jhtml" >指导性案例</a></li>

	<li><a href="http://dljc.ynfy.gov.cn:80/ssfw/index.jhtml" >诉讼服务</a></li>

        
	</ul>

</div>
		</div>

		<!-- sub_page_head end -->

		<div class="sswy_con ">

			<div class="sswy_con_top">

					<div class="layer">

						<h1 class="sswy_h1_box"><span class="sp_logo"></span >

							<span class="sp_title">剑川县人民法院</span>

							<span class="sp_a">>



							执行信息







<!--						失信被执行人-->

							</span>

						</h1>

						

						<div class="sswy_search_box_wrap">

							<div class="sswy_search_box">

							<form action="/search.jspx" id="search">

								<div class="search_menu">

									<div class="search_value_box">

										<span class="sp_gain_value">全站搜索</span>

										<span class="sp_mousedown"></span>

									</div>

									<dl class="search_con_nav">



										<dd onclick="document.getElementById('channelId2').value=8914">法院要闻</dd>


										<dd onclick="document.getElementById('channelId2').value=8919">法院公告</dd>


										<dd onclick="document.getElementById('channelId2').value=8928">裁判文书</dd>


										<dd onclick="document.getElementById('channelId2').value=8929">审判流程</dd>


										<dd onclick="document.getElementById('channelId2').value=8995">执行信息</dd>


										<dd onclick="document.getElementById('channelId2').value=9039">庭审视频</dd>


										<dd onclick="document.getElementById('channelId2').value=9041">指导性案例</dd>


										<dd onclick="document.getElementById('channelId2').value=9045">案件查询</dd>


										<dd onclick="document.getElementById('channelId2').value=9047">网上立案</dd>


										<dd onclick="document.getElementById('channelId2').value=9049">法规查询</dd>


										<dd onclick="document.getElementById('channelId2').value=9051">诉讼服务</dd>


										<dd onclick="document.getElementById('channelId2').value=15214">执行线索举报</dd>


										<dd onclick="document.getElementById('channelId2').value=15428">裁判文书公开规定</dd>



									</dl>

								</div>

								<div class="sswy_search_wrap">

									<span class="sp_search">

										

										<input type="hidden" name="channelId" id="channelId2" value=""/>

										

										<input type="text" name="q" id="sswy_search" value=""/>

										<a href="javascript:void(0)" class="search_btn" onclick="document.getElementById('search').submit()">搜&nbsp;索</a>

<!--										<input type="submit" value="搜  索" class="search_btn"/>-->

									</span>

								</div>

							</form>

								<!-- sswy_search_box end -->

							</div>

							<!-- sswy_search_box end -->	

						</div>

						<!-- sswy_search_box_wrap end -->

					</div>

					<!-- layer end -->

				</div>

				<!-- sswy_con_top end -->

			<div class="sswy_sub_con">

				<div class="sswy_sub_con_line_t  m0"></div>

				<div class="sswy_sub_con_area  m0">

					<h2 class="sswy_sub_h2">正文</h2>

				</div> 

				<div class="sswy_article_box">

					<div class="sswy_article_t">

						<h4 class="sswy_article_h4">失信被执行人名单</h4>

						<p class="p_article_time">2016-09-29 21:16:25　来源: 本站</p>

					</div>

					<!-- sswy_article_t end -->

					<div class="sswy_article_m">


						<p>
<table border="0" cellspacing="0" cellpadding="0" width="632" style="width: 474pt; border-collapse: collapse">
    <colgroup><col width="72" style="width: 54pt" /><col width="108" style="width: 81pt; mso-width-source: userset; mso-width-alt: 3456" /><col width="143" style="width: 107pt; mso-width-source: userset; mso-width-alt: 4576" /><col width="191" style="width: 143pt; mso-width-source: userset; mso-width-alt: 6112" /><col width="118" style="width: 89pt; mso-width-source: userset; mso-width-alt: 3776" /></colgroup>
    <tbody>
        <tr height="42" style="height: 31.5pt; mso-height-source: userset">
            <td class="xl65" height="42" width="72" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext 0.5pt solid; background-color: transparent; width: 54pt; height: 31.5pt; border-top: windowtext 0.5pt solid; border-right: windowtext 0.5pt solid"><font size="3" face="宋体">　</font></td>
            <td class="xl65" width="108" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 81pt; border-top: windowtext 0.5pt solid; border-right: windowtext 0.5pt solid"><font size="3" face="宋体">姓名/名称</font></td>
            <td class="xl65" width="143" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 107pt; border-top: windowtext 0.5pt solid; border-right: windowtext 0.5pt solid"><font size="3" face="宋体">&nbsp;&nbsp; 类型</font></td>
            <td class="xl65" width="191" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 143pt; border-top: windowtext 0.5pt solid; border-right: windowtext 0.5pt solid"><font size="3" face="宋体">执行案号</font></td>
            <td class="xl65" width="118" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 89pt; border-top: windowtext 0.5pt solid; border-right: windowtext 0.5pt solid"><font size="3" face="宋体">执行法院</font></td>
        </tr>
        <tr height="57" style="height: 42.75pt">
            <td class="xl66" height="57" width="72" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext 0.5pt solid; background-color: transparent; width: 54pt; height: 42.75pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">1</font></td>
            <td class="xl67" width="108" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 81pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">段四平</font></td>
            <td class="xl66" width="143" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 107pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">自然人</font></td>
            <td class="xl67" width="191" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 143pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">(2016)云2931执40号</font></td>
            <td class="xl67" width="118" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 89pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">剑川县人民法院</font></td>
        </tr>
        <tr height="57" style="height: 42.75pt">
            <td class="xl66" height="57" width="72" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext 0.5pt solid; background-color: transparent; width: 54pt; height: 42.75pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">2</font></td>
            <td class="xl67" width="108" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 81pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">景士华</font></td>
            <td class="xl66" width="143" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 107pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">自然人</font></td>
            <td class="xl67" width="191" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 143pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">(2016)云2931执70号</font></td>
            <td class="xl67" width="118" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 89pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">剑川县人民法院</font></td>
        </tr>
        <tr height="57" style="height: 42.75pt">
            <td class="xl66" height="57" width="72" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext 0.5pt solid; background-color: transparent; width: 54pt; height: 42.75pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">3</font></td>
            <td class="xl67" width="108" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 81pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">景荣廷</font></td>
            <td class="xl66" width="143" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 107pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">自然人</font></td>
            <td class="xl67" width="191" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 143pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">(2016)云2931执70号</font></td>
            <td class="xl67" width="118" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 89pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">剑川县人民法院</font></td>
        </tr>
        <tr height="57" style="height: 42.75pt">
            <td class="xl66" height="57" width="72" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext 0.5pt solid; background-color: transparent; width: 54pt; height: 42.75pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">4</font></td>
            <td class="xl67" width="108" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 81pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">景顺红</font></td>
            <td class="xl66" width="143" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 107pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">自然人</font></td>
            <td class="xl67" width="191" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 143pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">(2016)云2931执70号</font></td>
            <td class="xl67" width="118" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 89pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">剑川县人民法院</font></td>
        </tr>
        <tr height="57" style="height: 42.75pt">
            <td class="xl66" height="57" width="72" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext 0.5pt solid; background-color: transparent; width: 54pt; height: 42.75pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">5</font></td>
            <td class="xl67" width="108" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 81pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">金厚超</font></td>
            <td class="xl66" width="143" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 107pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">自然人</font></td>
            <td class="xl67" width="191" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 143pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">(2016)云2931执5号</font></td>
            <td class="xl67" width="118" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 89pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">剑川县人民法院</font></td>
        </tr>
        <tr height="57" style="height: 42.75pt">
            <td class="xl66" height="57" width="72" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext 0.5pt solid; background-color: transparent; width: 54pt; height: 42.75pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">6</font></td>
            <td class="xl67" width="108" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 81pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">陶鸿镳</font></td>
            <td class="xl66" width="143" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 107pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">自然人</font></td>
            <td class="xl67" width="191" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 143pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">(2016)云2931执5号</font></td>
            <td class="xl67" width="118" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 89pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">剑川县人民法院</font></td>
        </tr>
        <tr height="57" style="height: 42.75pt">
            <td class="xl66" height="57" width="72" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext 0.5pt solid; background-color: transparent; width: 54pt; height: 42.75pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">7</font></td>
            <td class="xl67" width="108" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 81pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">金厚超</font></td>
            <td class="xl66" width="143" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 107pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">自然人</font></td>
            <td class="xl67" width="191" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 143pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">(2016)云2931执14号</font></td>
            <td class="xl67" width="118" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 89pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">剑川县人民法院</font></td>
        </tr>
        <tr height="57" style="height: 42.75pt">
            <td class="xl66" height="57" width="72" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext 0.5pt solid; background-color: transparent; width: 54pt; height: 42.75pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">8</font></td>
            <td class="xl67" width="108" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 81pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">陶鸿镳</font></td>
            <td class="xl66" width="143" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 107pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">自然人</font></td>
            <td class="xl67" width="191" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 143pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">(2016)云2931执14号</font></td>
            <td class="xl67" width="118" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 89pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">剑川县人民法院</font></td>
        </tr>
        <tr height="57" style="height: 42.75pt">
            <td class="xl66" height="57" width="72" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext 0.5pt solid; background-color: transparent; width: 54pt; height: 42.75pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">9</font></td>
            <td class="xl67" width="108" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 81pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">剑川县绿色产业开发中心</font></td>
            <td class="xl66" width="143" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 107pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">法人或其他组织</font></td>
            <td class="xl67" width="191" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 143pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">(2015)剑法执字第00040号</font></td>
            <td class="xl67" width="118" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 89pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">剑川县人民法院</font></td>
        </tr>
        <tr height="76" style="height: 57pt">
            <td class="xl66" height="76" width="72" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext 0.5pt solid; background-color: transparent; width: 54pt; height: 57pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">10</font></td>
            <td class="xl67" width="108" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 81pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">剑川县景贤工贸有限责任公司</font></td>
            <td class="xl66" width="143" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 107pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">法人或其他组织</font></td>
            <td class="xl67" width="191" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 143pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">(2008)剑法执字第00037号</font></td>
            <td class="xl67" width="118" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 89pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">剑川县人民法院</font></td>
        </tr>
        <tr height="76" style="height: 57pt">
            <td class="xl66" height="76" width="72" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext 0.5pt solid; background-color: transparent; width: 54pt; height: 57pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">11</font></td>
            <td class="xl67" width="108" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 81pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">大理剑川量子投资开发有限责任公司</font></td>
            <td class="xl66" width="143" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 107pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">法人或其他组织</font></td>
            <td class="xl67" width="191" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 143pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">(2016)云2931执14号</font></td>
            <td class="xl67" width="118" style="border-bottom: windowtext 0.5pt solid; border-left: windowtext; background-color: transparent; width: 89pt; border-top: windowtext; border-right: windowtext 0.5pt solid"><font color="#333333" size="3" face="宋体">剑川县人民法院</font></td>
        </tr>
    </tbody>
</table>
</p>

					</div>


                        <br/>




					<!-- sswy_article_m end -->	

				</div>

				<!-- sswy_article_box end -->

			</div>

			<!-- sswy_sub_con end -->



		</div>

		<!-- sswy_con end -->

	</div>

	<!-- bg_bj end  -->

<div class="sswy_foot">

		<div class="sswy_foot_text">

			<p><script type="text/javascript">var cnzz_protocol = (("https:" == document.location.protocol) ? " https://" : " http://");document.write(unescape("%3Cspan id='cnzz_stat_icon_1253842156'%3E%3C/span%3E%3Cscript src='" + cnzz_protocol + "w.cnzz.com/q_stat.php%3Fid%3D1253842156' type='text/javascript'%3E%3C/script%3E"));</script> 技术支持：北京华宇信息技术有限公司</p>

		</div>

	</div>
	<!-- sswy_foot end -->

	<script type="text/javascript" src="/../r/cms/www/jchfy/js/jquery-1.8.2.min.js"></script>

	<script type="text/javascript" src="/../r/cms/www/jchfy/js/sswy.js"></script>

	<script type="text/javascript">

		$(document).ready(function(){

			if(typeof document.body.style.maxHeight === "undefined") {

					$(".sswy_tel_box  a ,.active em, .load  em, .sp_logo").addClass("png_bg");

				}



			});	

		//文本框获取失去焦点的方法

		$("#sswy_search").addFocus({

			textContent:"输入文书关键词查找",

			defaultColor:"#bababa",

			textColor:"#333"

		});

		//  底部技术支持

		$(".sswy_foot").addAdjustResize({

				background:"#2f81dc",

				mainWidth:990

		});	

	</script>

	<!--[if IE 6]>

	<script src="js/DD_belatedPNG_0.0.8a-min.js"></script>

	<script>

		DD_belatedPNG.fix('.png_bg');

	</script>

	<![endif]-->

	

</body>

</html>
    '''
    yn = YunNan(path='失信被执行人', list=s, detail=d)
    print(yn.sxbzx())
    pass
