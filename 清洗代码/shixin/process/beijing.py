import os
import sys
sys.path.append(os.path.abspath(__file__ + "/../../../../"))
from IKEA.shixin.process.base_process import Base
from IKEA.mysql.mysqlbase import MysqlBase
from IKEA.shixin.config import connecter
from pyquery import PyQuery as pq
from lxml import etree
from bs4 import BeautifulSoup
import re
from datetime import datetime


class BeiJing(Base):

    def __init__(self,**kwargs):
        super(BeiJing,self).__init__(**kwargs)
        self.html = etree.HTML(self.list)
        self.results = self.html.xpath('//td')
        self.name = self.results[1].xpath('./a/@title')[0] if self.results[1].xpath('./text()') else ''
        self.card_num = self.results[3].xpath('./text()')[0] if self.results[3].xpath('./text()') else ''
        self.case_code = self.results[5].xpath('./text()')[0] if self.results[5].xpath('./text()') else ''
        self.gist_id = self.results[6].xpath('./@title')[0] if self.results[6].xpath('./text()') else ''
        self.court_name = self.results[7].xpath('./text()')[0] if self.results[7].xpath('./text()') else ''
        self.reg_date = self.results[8].xpath('./text()')[0] if self.results[8].xpath('./text()') else None
        if self.reg_date:
            self.reg_date = datetime.strptime(self.reg_date,'%b %d, %Y')
            self.reg_date = datetime.strftime(self.reg_date,'%Y-%m-%d')

        self.resp = etree.HTML(self.detail)
        self.msg = {}
        trs = self.resp.xpath('//table[@class="table_list_03"]//tr')
        for tr in trs:
            rsts = tr.xpath('./td/text()')
            if len(rsts) == 2:
                key = rsts[0]
                value = rsts[1]
                self.msg[key] = value
        self.sex = self.msg.get('性别','').strip()
        self.age = self.msg.get('年龄','').strip()
        self.business_entity = self.msg.get('法定代表人或负责人','').strip()
        self.address = self.msg.get('被执行人地址','').strip()
        self.release_date = self.msg.get('认定日期','').strip()
        if self.release_date:
            self.release_date = datetime.strptime(self.release_date,'%b %d, %Y')
            self.release_date = datetime.strftime(self.release_date,'%Y-%m-%d')
        self.disrupt_type_name = self.msg.get('失信行为具体情形','').strip()
        self.duty = self.msg.get('生效法律文书确定的义务','').strip()
        self.gist_unit = self.msg.get('执行依据制作单位','').strip()

        self.area_name = '北京'
        self.source = self.path
    #
    def sxbzx(self):
        print('{}:{}'.format(datetime.now(), self.path))
        self.executive_person['name'] = self.name
        self.executive_person['case_code'] = self.case_code
        self.executive_person['court_name'] = self.court_name
        self.executive_person['age'] = self.age
        self.executive_person['sex'] = self.sex
        # self.executive_person['party_type_name'] = self.itype
        self.executive_person['reg_date'] = self.reg_date
        self.executive_person['card_num'] = self.card_num
        self.executive_person['gist_id'] = self.gist_id
        self.executive_person['gist_unit'] = self.gist_unit
        self.executive_person['reg_date'] = self.reg_date
        self.executive_person['duty'] = self.duty
        self.executive_person['disrupt_type_name'] = self.disrupt_type_name
        self.executive_person['business_entity'] = self.business_entity
        self.executive_person['publish_date'] = self.release_date
        self.executive_person['area_name'] = self.area_name
        self.executive_person['source'] = self.path
        # print(self.executive_person)
        self.executive_person['operator'] = 'wangfeng'
        # return self.executive_person
    #
    def xzgxf(self):
        print('{}:{}'.format(datetime.now(), self.path))
        # self.exposure_desk["exposure_type"] = self.exposure_type
        self.exposure_desk['name'] = self.name
        # self.exposure_desk['identity'] = self.identity
        self.exposure_desk['age'] = self.age
        self.exposure_desk['sex'] = self.sex
        self.exposure_desk['card_num'] = self.card_num
        self.exposure_desk['case_code'] = self.case_code
        self.exposure_desk['court_name'] = self.court_name
        # self.exposure_desk['limiting_cause'] = self.limiting_cause
        # self.exposure_desk['restricted_content'] = self.restricted_content
        self.exposure_desk['business_entity'] = self.business_entity
        self.exposure_desk['address'] = self.address
        self.exposure_desk['reg_date'] = self.reg_date
        self.exposure_desk['release_date'] = self.release_date
        # self.exposure_desk['case_status'] = self.case_status
        self.exposure_desk['gist_id'] = self.gist_id
        self.exposure_desk['gist_unit'] = self.gist_unit
        self.exposure_desk['source'] = self.source
        self.exposure_desk['operator'] = 'wangfeng'

        self.executive_announcement['operator'] = 'wangfeng'
        # print(self.exposure_desk)
        super().split_ex()
        # return self.exposure_desk
    #
    #
    def xzcj(self):
        return self.xzgxf()
    #
    def xztzb(self):
        return self.xzgxf()



if __name__ == '__main__':
    s = '''
    <tr>
<td>394</td>
<td class="td_even" title="李红亮">
<a href="/zxxx/explain.htm?zxxxlx=100013002&amp;xxid=1800000009120" title="李红亮">李红亮</a>
</td>
<td>居民身份证</td>
<td class="td_even"> 340822198203032413</td>
<td>限制出境</td>
<td class="td_even">2011年通执字第05093号</td>
<td title="2011年通民初字第04342号">2011年通民初字第04342...</td>
<td class="td_even">北京市通州区人民法院</td>
<td>Aug 15, 2011</td>
</tr>
    '''
    d = '''
       <!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta http-equiv="X-UA-Compatible" content="IE=edge" />
<title>北京法院审判信息网-执行信息</title>
<link rel="stylesheet" type="text/css" href="/pub/blueskin/css/reset.css" media="all" />
		<link rel="stylesheet" type="text/css" href="/pub/blueskin/css/global.css" media="all" />
		<link rel="stylesheet" type="text/css" href="/pub/blueskin/css/common.css" media="all" />
		<link rel="stylesheet" type="text/css" href="/pub/blueskin/css/mainnav.css" media="all" />
		<link type="text/css" rel="stylesheet" href="/pub/blueskin/css/QRCode.css" />
		<link type="text/css" rel="stylesheet" href="/jq/jquery-ui/jquery-ui-1.9.2.custom.css" />
        <link type="text/css" rel="stylesheet" href="/pub/blueskin/css/ui_date_plugin.css" />
    <script type="text/javascript">
    var contextPath = "";
</script>
<script type="text/javascript" src="/jq/jquery-1.8.3.js"></script>
<script type="text/javascript" src="/jq/smartpaginator/jquery.pagination.js"></script>
<script type="text/javascript" src="/pub/comm.js"></script></head>
<body>
  <div class="contain">
  <!-- 右侧工具栏  首页不显示-->
<div class="fixed_service">
        <ul class="ul_fixed">
            <li  class="first"> 
                <span class="sp_arrow">
                    <a href="/feedback/my/contact.htm" class="a_person" target="_blank"><span class="sp_icon">法官</span></a>
                    <a href="/feedback/my/advisory.htm"  target="_blank">咨询</a>
                    <a href="/feedback/my/complaint.htm" class ="a_last" target="_blank">投诉</a>
                </span>
            </li>
            <li>
                <span class="sp_arrow">
                    <a href="/pro/fwpj/fwpjlst.htm" class="a_judge " target="_blank"><span class="sp_icon">个人评价</span></a>
                </span>
            </li></ul>   
        <!-- ul_fixed end -->
    </div><div class="header">
    <div class="header_t">
        <div class="header_in">
            <div class="header_info">
                  <span class="sp_login_btn">
                        <a href='/login/pro.htm' class="a_login">登录</a>
                        </span>
                    <span class="sp_count">网站访问量：322311225</span> 
            </div>
            <!-- header_info end -->
            <div class="index_logo">
                <a href='/' class="a_logo"></a>
            </div>
            <a class="index_header_QRcode addQRCodebtn">
            </a>            
        </div>
        <!-- header_in end -->
    </div>
    <!-- header_m end -->
    <div class="header_b">
        <div class="header_b_in" id="headerId">
            <ul class="main_nav" >
                <li class="li_item first_item"><a href='/'
                    class="a_li_item">首页</a>
                </li>
                <li class="li_item "><a href='/fyyw/index.htm'
                    class="a_li_item">法院要闻</a>
                    <div class="sub_nav_con">
	<div class="sub_nav_con_m">
		<div class="sub_nav_con_t">
			<div class="layer">
				<div class="column_sub_nav ml38">
					<dl class="dl_03">
						<dt>法院要闻</dt>
						<dd>
							<ul class="ul_news_05">
							     <li>
							             <a href="/article/newsDetail.htm?NId=75003034&channel=100001001">北京法院谋划下半年工作</a>
                                     </li>
							     <li>
							             <a href="/article/newsDetail.htm?NId=75003021&channel=100001001">海淀法院举行第三批特邀人民调解员聘任暨山后人民法庭、上地人民法庭诉前调解室揭牌仪式</a>
                                     </li>
							     <li>
							             <a href="/article/newsDetail.htm?NId=75002959&channel=100001001">海淀法院首推“三全五化”执行机制改革 半年发案款9.7亿</a>
                                     </li>
							     <li>
							             <a href="/article/newsDetail.htm?NId=75002938&channel=100001001">国家法官学院与北京高院签订协议促进双向交流合作</a>
                                     </li>
							     </ul>
							<a href="/fyyw/index.htm?c=100001001" class="a_dd_more">更多......</a>
						</dd>
					</dl>
					<!-- dl_03 end -->
				</div>
				<!-- column_sub_nav end -->
				<div class="column_sub_nav ml48">
					<dl class="dl_03">
						<dt>重要通知</dt>
						<dd>
							<ul class="ul_news_05">
							    <li>
                                         <a href="/article/newsDetail.htm?NId=75002801&channel=100001011">最高人民法院、最高人民检察院关于办理侵犯公民个人信息刑事案件适用法律若干问题的解释</a>
                                     </li>
                                 <li>
                                         <a href="/article/newsDetail.htm?NId=75002800&channel=100001011">最高人民法院关于落实司法责任制完善审判监督管理机制的意见（试行）</a>
                                     </li>
                                 <li>
                                         <a href="/article/newsDetail.htm?NId=75002799&channel=100001011">最高人民法院关于加强各级人民法院院庭长办理案件工作的意见（试行）</a>
                                     </li>
                                 <li>
                                         <a href="/article/newsDetail.htm?NId=70002800&channel=100001011">最高人民法院关于民事执行中财产调查若干问题的规定</a>
                                     </li>
                                 </ul>
							<a href="/fyyw/index.htm?c=100001011" class="a_dd_more">更多......</a>
						</dd>
					</dl>
					<!-- dl_03 end -->
				</div>
				<!-- column_sub_nav end -->
				<div class="column_sub_nav ml48">
					<dl class="dl_03">
						<dt>法院工作报告</dt>
						<dd>
							<ul class="ul_news_05">
								<li>
                                         <a href="/article/newsDetail.htm?NId=55003465&channel=100001012">北京市高级人民法院2016年工作报告</a>
                                     </li>
                                 <li>
                                         <a href="/article/newsDetail.htm?NId=55001802&channel=100001012">北京市高级人民法院2015年工作报告</a>
                                     </li>
                                 <li>
                                         <a href="/article/newsDetail.htm?NId=55001088&channel=100001012">北京市高级人民法院关于知识产权司法保护情况的报告</a>
                                     </li>
                                 <li>
                                         <a href="/article/newsDetail.htm?NId=55000085&channel=100001012">北京市高级人民法院2014工作报告</a>
                                     </li>
                                 </ul>
							<a href="/fyyw/index.htm?c=100001012" class="a_dd_more">更多......</a>
						</dd>
					</dl>
					<!-- dl_03 end -->
				</div>
				<!-- column_sub_nav end -->
			</div>
			<!-- layer end -->
		</div>
		<!-- sub_nav_con_t end -->
	</div>
	<!-- sub_nav_con_m end -->
</div>
<!-- sub_nav_con end --></li>
                <li class="li_item "><a href='/ktgg/index.htm'
                    class="a_li_item">公告公示</a>
                    <div class="sub_nav_con"  style="display:;">
    <div class="sub_nav_con_m">
           <div class="sub_nav_con_t">
                    <div class="layer p5_0_0_10">
                        <ul class="ul_link_03">
                               <li>
                                     <a href="/ktgg/index.htm" class="a_btn_01">
                                          <span class="sp_r">
                                                <span class="sp_m">
                                                      <span class="sp_arrow">开庭公告</span>
                                                </span>
                                            </span>
                                      </a>
                                </li>
                                 <li>
                                        <a href="/fygg/index.htm?c=100002004"  class="a_btn_01">
                                            <span class="sp_r">
                                                  <span class="sp_m">
                                                       <span class="sp_arrow">鉴拍公告</span>
                                                  </span>
                                             </span>
                                         </a>
                                   </li>
                                   <li>
                                         <a href="/fygg/index.htm?c=100002005"  class="a_btn_01">
                                              <span class="sp_r">
                                                     <span class="sp_m">
                                                          <span class="sp_arrow">拍卖公告</span>
                                                     </span>
                                               </span>
                                          </a>
                                   </li>
                                    <li>
                                          <a href="/fygg/index.htm?c=100002006"  class="a_btn_01">
                                                 <span class="sp_r">
                                                      <span class="sp_m">
                                                            <span class="sp_arrow">变卖公告</span>
                                                      </span>
                                                 </span>
                                           </a>
                                    </li>
                                    <li>
                                            <a href="/fygg/index.htm?c=100002007"  class="a_btn_01">
                                                   <span class="sp_r">
                                                        <span class="sp_m">
                                                                <span class="sp_arrow">破产管理人</span>
                                                         </span>
                                                    </span>
                                              </a>
                                       </li>
                                        <li>
                                             <a href="/fygg/index.htm?c=100002009"  class="a_btn_01">
                                                        <span class="sp_r">
                                                            <span class="sp_m">
                                                                <span class="sp_arrow">悬赏公告</span>
                                                            </span>
                                                        </span>                                                     
                                              </a>
                                          </li>
                                           <li>
                                                    <a href="/fygg/index.htm?c=100002008"  class="a_btn_01">
                                                        <span class="sp_r">
                                                            <span class="sp_m">
                                                                <span class="sp_arrow">其他公告</span>
                                                            </span>
                                                        </span>     
                                                    </a>
                                            </li>
                                            <li>
                                                 <a href="/bggs/index.htm"  class="a_btn_01">
                                                        <span class="sp_r">
                                                            <span class="sp_m">
                                                                <span class="sp_arrow">减刑假释类公示</span>
                                                            </span>
                                                        </span>     
                                                    </a>
                                            </li>
                                      </ul>
                                      <!-- ul_link_03 end -->
                               </div>
                               <!-- layer end -->
                      </div>
                      <!-- sub_nav_con_t end -->
          </div>
          <!-- sub_nav_con_m end -->
 </div>  
<!-- sub_nav_con end --></li>
                <li class="li_item "><a href='/cpws/index.htm'
                    class="a_li_item">裁判文书</a>
                     <div class="sub_nav_con"  style="display:;" id='sub_nav_writ'>
             <div class="sub_nav_con_m">
                            <div class="sub_nav_con_t">
                                        <div class="layer p25_0_0_28">
                                            <div class="grid_layout_600 fl">
                                            <form id="navSearchForm" name="navSearchForm" action="/cpws/index.htm" target="_blank">
                                                <span class="sp_ipt_wrap m0_0_24_40">
                                                    <label for="">案由</label>
                                                    <input type="text" name="ay"  value="" />
                                                </span>
                                                <span class="sp_ipt_date_wrap m0_0_24_40">
                                                    <label for="">生效日期</label>
                                                    <input type="text" name="startCprq"  id="navStartCprq" value="" class="date_input" />
                                                    <span> 至</span>
                                                    <input type="text" name="endCprq"  id="navEndCprq" value="" class="date_input"  />
                                                </span>
                                                <span class="sp_ipt_wrap m0_0_24_40">
                                                    <label for="">案号</label>
                                                    <input type="text" name="ah"  value="" />
                                                </span>
                                                <a href="javascript:void(0);" class="a_search_btn m0_0_24_40" id="navSearchSubmitButton">搜&nbsp;索</a>
                                                                                                <span class="sp_ipt_blank_wrap m0_0_24_40">
                                                </span>
                                                <span class="sp_ipt_blank_wrap m0_0_24_40" id="navCpwsTips">
                                                </span>
                                                </form>
                                            </div>
                                            <!-- grid_layout_600 end  -->
                                            <div class="grid_layout_300  fl">
                                                <div class="layer pb20">
                                                    <a href="/cpws/explain.htm?c=100019003" class="a_btn_01">
                                                        <span class="sp_r">
                                                            <span class="sp_m">
                                                                <span class="sp_arrow  grid_layout_210" >裁判文书公开的技术处理标准</span>
                                                            </span>
                                                        </span>                                                     
                                                    </a>    
                                                </div>
                                                 <!-- layer end  -->
                                                <div class="layer pb20">
                                                    <a href="/cpws/explain.htm?c=100019006" class="a_btn_01">
                                                        <span class="sp_r">
                                                            <span class="sp_m">
                                                                <span class="sp_arrow grid_layout_210" >裁判文书公开信息的查询方法</span>
                                                            </span>
                                                        </span>     
                                                    </a>
                                                </div>  
                                                 <!-- layer end  -->
                                                <div class="layer">
                                                    <a href="/cpws/explain.htm?c=100019002" class="a_btn_01 ">
                                                        <span class="sp_r">
                                                            <span class="sp_m">
                                                                <span class="sp_arrow grid_layout_210">裁判文书的公开范围</span>
                                                            </span>
                                                        </span>     
                                                    </a>
                                                </div>
                                                <!-- layer end -->
                                                
                                            </div>
                                            <!-- grid_layout_300 end -->                            
                                        </div>
                                        <!-- layer end -->
                                    </div>
                                    <!-- sub_nav_con_t end -->
                                </div>
                                <!-- sub_nav_con_m end -->
</div>  
 <!-- sub_nav_con end -->
 <script type="text/javascript">
 $("#navSearchSubmitButton").click(function(e){
     /* 日期正则表达式 */
    var datePat = /^(19[7-9]\d|20\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[1-2]\d|3[0-1])$/;
     e.preventDefault();
     $("#navCpwsTips").html();
     var startCprq = $("#navStartCprq").val();
     var endCprq = $("#navEndCprq").val();
     if (startCprq.length>0 &&!datePat.test(startCprq)) {
       $("#navCpwsTips").html("生效日期的起始日期格式错误：格式为yyyy-MM-dd，范围为[1970-01-01 ~ 2099-12-31]。");
       return;
     }
     if (endCprq.length>0 &&!datePat.test(endCprq)) {
       $("#navCpwsTips").html("生效日期的截止日期格式错误：格式为yyyy-MM-dd，范围为[1970-01-01 ~ 2099-12-31]。");
       return;
     }
     if (endCprq.length>0 && startCprq.length>0 &&startCprq.localeCompare(endCprq) == 1) {
       $("#navCpwsTips").html("生效日期的起始日期不能大于截止日期。");
       return;
     }
     $("#navSearchForm").submit();
 });
 </script></li>
                <li class="li_item "><a href='/splc/index.htm'
                    class="a_li_item">审判流程</a>
                     <div class="sub_nav_con"  style="display:;">
    <div class="sub_nav_con_m">
          <div class="sub_nav_con_t">
             <div class="layer pl28">
                   <div class="grid_layout_600 fl">
                           <div class="grid_layout_265 fl">
                                     <dl class="dl_03">
                                                <dt>北京法院指导文件 </dt>
                                                        <dd>
                                                            <table class="table_layout_01">
                                                                <tr>
                                                                    <td class="td_01">
                                                                        <ul class="ul_news_05">
                                                                            <li><a href="/splc/wjindex.htm?c=100014001">民事审判业务规范 </a></li>
                                                                            <li><a href="/splc/wjindex.htm?c=100014002">商事审判业务规范</a></li>
                                                                            <li><a href="/splc/wjindex.htm?c=100014003">知识产权审判业务规范</a></li>
                                                                            <li><a href="/splc/wjindex.htm?c=100014004">刑事审判业务规范</a></li>
                                                                            <li><a href="/splc/wjindex.htm?c=100014009">审判管理</a></li>
                                                                        </ul>
                                                                    </td>
                                                                    <td>
                                                                        <ul class="ul_news_05">
                                                                            <li><a href="/splc/wjindex.htm?c=100014005">行政审判业务规范</a></li>
                                                                            <li><a href="/splc/wjindex.htm?c=100014006">执行业务规范</a></li>
                                                                            <li><a href="/splc/wjindex.htm?c=100014007">国家赔偿业务规范</a></li>
                                                                            <li><a href="/splc/wjindex.htm?c=100014008">未成年审判业务规范</a></li>
                                                                        </ul>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </dd>
                                                    </dl>
                                                    <!-- dl_03 end -->
                                                </div>
                                                <!-- grid_layout_265 end -->
                                                <div class="grid_layout_265 fl ml48">
                                                    <dl class="dl_03">
                                                        <dt>最高法院指导文件 </dt>
                                                        <dd>
                                                            <table class="table_layout_01">
                                                                <tr>
                                                                    <td  class="td_01">
                                                                        <ul class="ul_news_05">
                                                                            <li><a href="/splc/wjindex.htm?c=100021001">民事审判业务规范 </a></li>
                                                                            <li><a href="/splc/wjindex.htm?c=100021002">商事审判业务规范</a></li>
                                                                            <li><a href="/splc/wjindex.htm?c=100021003">知识产权审判业务规范</a></li>
                                                                            <li><a href="/splc/wjindex.htm?c=100021004">刑事审判业务规范</a></li>
                                                                            <li><a href="/splc/wjindex.htm?c=100021009">其他</a></li>
                                                                        </ul>
                                                                    </td>
                                                                    <td>
                                                                        <ul class="ul_news_05">
                                                                            <li><a href="/splc/wjindex.htm?c=100021005">行政审判业务规范</a></li>
                                                                            <li><a href="/splc/wjindex.htm?c=100021006">执行业务规范</a></li>
                                                                            <li><a href="/splc/wjindex.htm?c=100021007">国家赔偿业务规范</a></li>
                                                                            <li><a href="/splc/wjindex.htm?c=100021008">未成年审判业务规范</a></li>
                                                                        </ul>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </dd>
                                                    </dl>
                                                    <!-- dl_03 end -->
                                                </div>
                                                <!-- grid_layout_265 end -->
                                            </div>
                                            <!-- grid_layout_600 end  -->
                                            <div class="grid_layout_250  fl ml60">
                                                <div class="layer pt40">
                                                    <a href="/splc/explain.htm?c=100019001" class="a_btn_01">
                                                        <span class="sp_r">
                                                            <span class="sp_m">
                                                                <span class="sp_arrow  grid_layout_160" >审判流程公开范围</span>
                                                            </span>
                                                        </span>                                                     
                                                    </a>    
                                                </div>
                                                 <!-- layer end  -->
                                                <div class="layer pt28">
                                                    <a href="/splc/explain.htm?c=100019005" class="a_btn_01">
                                                        <span class="sp_r">
                                                            <span class="sp_m">
                                                                <span class="sp_arrow grid_layout_160" >审判流程查询方法</span>
                                                            </span>
                                                        </span>     
                                                 </a>
                                     </div>  
                                     <!-- layer end  -->
                             </div>
                             <!-- grid_layout_300 end -->                            
                     </div>
                     <!-- layer end -->
            </div>
           <!-- sub_nav_con_t end -->
       </div>
       <!-- sub_nav_con_m end -->
</div>  
<!-- sub_nav_con end -->    </li>
                <li class="li_item li_item_on">
                	<a href='/zxxx/indexOld.htm?zxxxlx=100013001'class="a_li_item">执行信息</a> 
                     <link rel="stylesheet" type="text/css" href="/pub/blueskin/css/zxxx.css" media="all" />
  <div class="sub_nav_con"  style="display:;">
        <div class="sub_nav_con_m">
            <div class="sub_nav_con_t">
                <div class="layer p20_0_0_28">
                    <div class="grid_layout_600 fl">
                        <form id="navZxxxSearchForm" name="navZxxxSearchForm" action="/zxxx/indexOld.htm" target="_blank">
	                        <span class="sp_ipt_wrap_ajxxlx m0_0_24_40" id="ajxxlxSearch">
	                            <label for="">信息类型</label>
	                            <span class="ajxxlxTarget" id="ajxxlxTarget">失信</span>
	                            <input type="hidden" name="ajxxlx" id="ajxxlx_value" value="1" />
	                            <span class="sp_mousedown_ajxxlx" id="sp_mousedown_ajxxlx">&nbsp;</span>
	                            <dl class="search_con_nav" id="search_con_nav_ajxxlx">
                                    <dd value="1">失信</dd>
                                    <dd value="2">终本</dd>
                                </dl>
	                        </span>
	                        <span class="sp_ipt_wrap_zxxxzl m0_0_24_40" id="zxxxzlSearch">
	                            <label for="">失信范围</label>
	                            <span class="zxxxzlTarget" id="zxxxzlTarget">失信被执行人</span>
	                            <input type="hidden" name="zxxxlx" id="zxxxzl_value" value="100013001" />
	                            <span class="sp_mousedown_zxxxzl" id="sp_mousedown_zxxxzl">&nbsp;</span>
	                            <dl class="search_con_nav" id="search_con_nav_header">
                                    <dd value="100013001">失信被执行人</dd>
                                    <dd value="100013002">限制出境被执行人</dd>
                                    <dd value="100013004">限制高消费被执行人</dd>
                                    <dd value="100013003">限制招投标被执行人</dd>
                                </dl>
	                        </span>
	                        <span class="sp_ipt_wrap_plus_bzxrzl m0_0_24_40" id="bzxrzlSearch">
	                            <label for="" class="bzxrzl_lable">全部</label>
	                            <span class="sp_mousedown_bzxrzl" id="sp_mousedown_bzxrzl">&nbsp;</span>
	                            <input type="text" name="bzxrxm"  value="" />
	                            <input type="hidden" name="bzxrlx" id="bzxrzl_value"  value="" />
	                            <dl class="search_con_nav" id="search_con_nav_bzxrzl">
	                                <dd value="">全部</dd>
	                                <dd value="1">自然人</dd>
	                                <dd value="2,3">法人或其他组织</dd>
	                            </dl>
	                            <!-- search_con_nav end -->
	                        </span>
	                        <span class="sp_ipt_wrap m0_0_24_40">
                                <label for="">案号</label>
                                <input type="text" name="ah"  value="" />
                            </span>
                        </form>
                        <a href="javascript:void(0);" id="zxxx_header_submit" class="a_search_btn m0_0_24_40" style="float:right;position:relative;left:-88px;">搜&nbsp;索</a>
                    </div>
                    <!-- grid_layout_600 end  -->
                    <div class="grid_layout_300  fl ml15">
                        <div class="layer pb20">
                            <a href="/zxxx/detailed.htm?c=100019007&zxxxlx=100013001" class="a_btn_01">
                                <span class="sp_r">
                                    <span class="sp_m">
                                        <span class="sp_arrow  grid_layout_210" >执行信息公开信息的查询方法</span>
                                    </span>
                                </span>                                                     
                            </a>    
                        </div>
                         <!-- layer end  -->
                        <div class="layer ">
                            <a href="/zxxx/detailed.htm?c=100019004&zxxxlx=100013001" class="a_btn_01">
                                <span class="sp_r">
                                    <span class="sp_m">
                                        <span class="sp_arrow grid_layout_210" >执行信息的公开范围</span>
                                    </span>
                                </span>     
                            </a>
                        </div>  
                         <!-- layer end  -->    
                    </div>
                    <!-- grid_layout_300 end -->                            
                </div>
                <!-- layer end -->
            </div>
            <!-- sub_nav_con_t end -->
        </div>
        <!-- sub_nav_con_m end -->
    </div>  
<!-- sub_nav_con end -->

<script type="text/javascript">
$(document).ready(function() {
	$("#ajxxlxSearch").addSelect({
        triggerEleId:"sp_mousedown_ajxxlx",
        searchContentContain:".search_con_nav", 
        addHoverClass:"dd_hover",
        getValueClass:".ajxxlxTarget"
    });
    $("#bzxrzlSearch").addSelect({
        triggerEleId:"sp_mousedown_bzxrzl",
        searchContentContain:".search_con_nav", 
        addHoverClass:"dd_hover",
        getValueClass:".bzxrzl_lable"
    });
    $("#zxxxzlSearch").addSelect({
        triggerEleId:"sp_mousedown_zxxxzl",
        searchContentContain:".search_con_nav", 
        addHoverClass:"dd_hover",
        getValueClass:".zxxxzlTarget"
    });
    $("#search_con_nav_bzxrzl").children("dd").each(function() {
        $(this).click(function() {
            $("#bzxrzl_value").attr("value",$(this).attr("value"));
        });
    });
    $("#search_con_nav_header").children("dd").each(function() {
        $(this).click(function() {
            $("#zxxxzl_value").attr("value",$(this).attr("value"));
        });
    });
    $("#search_con_nav_ajxxlx").children("dd").each(function() {
        $(this).click(function() {
            $("#ajxxlx_value").attr("value",$(this).attr("value"));
            if($("#ajxxlx_value").val()==2){
            	$("#zxxxzlTarget").text("");
            	$("#sp_mousedown_zxxxzl").hide();
            	$("#zxxxzl_value").val("100013006");
            }
            if($("#ajxxlx_value").val()==1){
            	$("#zxxxzlTarget").text("失信被执行人");
            	$("#sp_mousedown_zxxxzl").show();
            }
        });
    });
    $("#zxxx_header_submit").click(function(e){
    	if(document.getElementById("zxxxzl_value").value!=100013001){
    		document.navZxxxSearchForm.action="/zxxx/indexOld.htm";
    	}
        e.preventDefault();
        $("#navZxxxSearchForm").submit();
    })
});

</script></li>
                <li class="li_item "><a href='/fgxx/index.htm'
                    class="a_li_item">法官信息</a>
                    <div class="sub_nav_con"  style="display:;">
                                <div class="sub_nav_con_m">
                                    <div class="sub_nav_con_t">
                                        <div class="layer p15_0_0_28">
                                            <div class="grid_layout_135 fl pt15 posr999">
                                                <a href="/fgxx/detail.htm?court=1&channel=100017002" class="a_btn_v_01  ml25">
                                                    <span class="sp_t">
                                                        <span class="sp_b">
                                                            <span class="sp_m">
                                                         北京市高级人民法院
                                                            </span>
                                                        </span>
                                                    </span>
                                                </a>    
                                                <span class="sp_btn_v_01_arrow"></span>
                                            </div>
                                            <!-- grid_layout_135 end  -->
                                            <div class="grid_layout_780 fl ">
                                                <div class="grid_layout_170 fl">
                                                    <dl class="dl_03">
                                                        <dt><a href="/fgxx/detail.htm?court=2&channel=100036002">北京市第一中级人民法院</a> </dt>
                                                        <dd>
                                                            <ul class="ul_news_05">
                                                                <li><a href="/fgxx/detail.htm?court=6&channel=100126002"> 北京市海淀区人民法院</a></li>
                                                                <li><a href="/fgxx/detail.htm?court=5&channel=100096002">北京市石景山区人民法院</a></li>
                                                                <li><a href="/fgxx/detail.htm?court=7&channel=100156002">北京市门头沟区人民法院</a></li>
                                                                <li><a href="/fgxx/detail.htm?court=9&channel=100216002">北京市昌平区人民法院</a></li>
                                                                <li><a href="/fgxx/detail.htm?court=11&channel=100276002">北京市延庆区人民法院</a></li>
                                                            </ul>
                                                        </dd>
                                                    </dl>
                                                    <!-- dl_03 end -->
                                                </div>
                                                <!-- grid_layout_170 end -->
                                                <div class="grid_layout_170 fl ml30">
                                                    <dl class="dl_03">
                                                        <dt><a href="/fgxx/detail.htm?court=12&channel=100306002">北京市第二中级人民法院</a></dt>
                                                        <dd>
                                                            <ul class="ul_news_05">
                                                                <li><a href="/fgxx/detail.htm?court=13&channel=100336002">北京市东城区人民法院</a></li>
                                                                <li><a href="/fgxx/detail.htm?court=3&channel=100066002">北京市西城区人民法院</a></li>
                                                                <li><a href="/fgxx/detail.htm?court=16&channel=100396002">北京市丰台区人民法院</a></li>
                                                                <li><a href="/fgxx/detail.htm?court=8&channel=100186002">北京市房山区人民法院</a></li>
                                                                <li><a href="/fgxx/detail.htm?court=10&channel=100246002">北京市大兴区人民法院</a></li>
                                                            </ul>
                                                        </dd>
                                                    </dl>
                                                    <!-- dl_03 end -->
                                                </div>
                                                <!-- grid_layout_170 end -->
                                                <div class="grid_layout_170 fl ml30">
                                                    <dl class="dl_03">
                                                        <dt><a href="/fgxx/detail.htm?court=29&channel=100636002">北京市第三中级人民法院</a></dt>
                                                        <dd>
                                                            <ul class="ul_news_05">
                                                                <li><a href="/fgxx/detail.htm?court=15&channel=100366002">北京市朝阳区人民法院</a></li>
                                                                <li><a href="/fgxx/detail.htm?court=18&channel=100456002">北京市通州区人民法院</a></li>
                                                                <li><a href="/fgxx/detail.htm?court=17&channel=100426002">北京市顺义区人民法院</a></li>
                                                                <li><a href="/fgxx/detail.htm?court=20&channel=100516002">北京市怀柔区人民法院</a></li>
                                                                <li><a href="/fgxx/detail.htm?court=19&channel=100486002">北京市平谷区人民法院</a></li>
                                                                <li><a href="/fgxx/detail.htm?court=21&channel=100546002">北京市密云区人民法院</a></li>
                                                            </ul>
                                                        </dd>
                                                    </dl>
                                                    <!-- dl_03 end -->
                                                </div>
                                                
                                                <div class="grid_layout_170 fl ml30">
                                                    <dl class="dl_03">
                                                        <dt><a href="/fgxx/detail.htm?court=22&channel=100576002">北京市第四中级人民法院</a></dt>
                                                        <dd>
                                                            <ul class="ul_news_05">
                                                                <li><a href="/fgxx/detail.htm?court=23&channel=100606002">北京铁路运输法院</a></li>
                                                            </ul>
                                                        </dd>
                                                    </dl>
                                                    <!-- dl_03 end -->
                                                </div>
                                                <!-- grid_layout_170 end -->
                                                
                                                 <div class="grid_layout_170 fl ml30">
                                                    <dl class="dl_03">
                                                        <dt><a href="/fgxx/detail.htm?court=30&channel=100576002">北京知识产权法院</a></dt>
                                                        <dd>
                                                            <ul class="ul_news_05">
                                                            </ul>
                                                        </dd>
                                                    </dl>
                                                    <!-- dl_03 end -->
                                                </div>
                                                <!-- grid_layout_170 end -->
                                                
                                               
                                                
                                            </div>
                                            <!-- grid_layout_780 end -->                            
                                        </div>
                                        <!-- layer end -->
                                    </div>
                                    <!-- sub_nav_con_t end -->
                                </div>
                                <!-- sub_nav_con_m end -->
                            </div>  
                    <!-- sub_nav_con end -->    </li>
                <li class="li_item  "><a href='/mcxx/index.htm'
                    class="a_li_item">名册信息</a>
                   <div class="sub_nav_con"  style="display:;">
    <div class="sub_nav_con_m">
        <div class="sub_nav_con_t">
            <div class="layer pl35">
                <div class="grid_layout_550 fl">
                    <div class="grid_layout_230 fl">
                        <dl class="dl_03">
                            <dt><a href="/mcxx/index.htm?c=001">人民陪审员名册</a> </dt>
                            <dd>
                                <ul class="ul_news_05">
                                    <li><a href="/mcxx/detail.htm?court=2&channel=100038001&current=001">北京市第一中级人民法院人民陪审员名册 </a></li>
                                    <li><a href="/mcxx/detail.htm?court=12&channel=100308001&current=001">北京市第二中级人民法院人民陪审员名册</a></li>
                                    <li><a href="/mcxx/detail.htm?court=29&channel=100638001&current=001">北京市第三中级人民法院人民陪审员名册</a></li>
                                    <li><a href="/mcxx/detail.htm?court=13&channel=100338001&current=001">北京市东城区人民法院人民陪审员名册</a></li>
                                </ul>
                                <a href="/mcxx/index.htm?c=001" class="a_dd_more">更多......</a>
                            </dd>
                        </dl>
                        <!-- dl_03 end -->
                    </div>
                    <!-- grid_layout_265 end -->
                    <div class="grid_layout_230 fl ml60">
                        <dl class="dl_03">
                            <dt><a href="/mcxx/index.htm?c=002">特邀调解组织和特邀调解员名册</a></dt>
                            <dd>
                                <ul class="ul_news_05">
                                	<li><a href="/mcxx/detail.htm?court=1&channel=100012002&current=002">北京市高级人民法院特邀调解组织和特邀调解员名册 </a></li>
                                    <li><a href="/mcxx/detail.htm?court=2&channel=100038002&current=002">北京市第一中级人民法院特邀调解组织和特邀调解员名册 </a></li>
                                    <li><a href="/mcxx/detail.htm?court=12&channel=100308002&current=002">北京市第二中级人民法院特邀调解组织和特邀调解员名册</a></li>
                                    <li><a href="/mcxx/detail.htm?court=29&channel=100638002&current=002">北京市第三中级人民法院特邀调解组织和特邀调解员名册</a></li>             
                                </ul>
                                <a href="/mcxx/index.htm?c=002" class="a_dd_more">更多......</a> 
                            </dd>
                        </dl>
                        <!-- dl_03 end -->
                    </div>
                    <!-- grid_layout_265 end -->
                </div>
                <!-- grid_layout_600 end  -->
                <div class="grid_layout_300  fl ml80">
                    <div class="layer pt20">
                        <a href="/mcxx/detail.htm?channel=100012003" class="a_btn_01">
                            <span class="sp_r">
                                <span class="sp_m">
                                    <span class="sp_arrow  grid_layout_210" >评估入选机构名册</span>
                                </span>
                            </span>                                                     
                        </a>    
                    </div>
                     <!-- layer end  -->
                    <div class="layer pt20">
                        <a href="/mcxx/detail.htm?channel=100012004" class="a_btn_01">
                            <span class="sp_r">
                                <span class="sp_m">
                                    <span class="sp_arrow grid_layout_210" >拍卖入选机构名册</span>
                                </span>
                            </span>     
                        </a>
                    </div>  
                     <!-- layer end  -->
                    <div class="layer pt20">
                        <a href="/mcxx/detail.htm?channel=100012005" class="a_btn_01">
                            <span class="sp_r">
                                <span class="sp_m">
                                    <span class="sp_arrow grid_layout_210" >鉴定入选机构名册</span>
                                </span>
                            </span>     
                        </a>
                    </div>  
                     <!-- layer end  -->
                    <div class="layer pt20">
                        <a href="/mcxx/detail.htm?channel=100012006" class="a_btn_01">
                            <span class="sp_r">
                                <span class="sp_m">
                                    <span class="sp_arrow grid_layout_210" >信用担保公司名册</span>
                                </span>
                            </span>     
                        </a>
                    </div>  
                     <!-- layer end  -->
                </div>
                <!-- grid_layout_300 end -->                            
            </div>
            <!-- layer end -->
        </div>
        <!-- sub_nav_con_t end -->
    </div>
    <!-- sub_nav_con_m end -->
</div>  
<!-- sub_nav_con end -->        </li>
                <li class="li_item  "><a href='/zdal/index.htm'
                    class="a_li_item ">参阅案例</a>
                    <div class="sub_nav_con"  style="display:;">
    <div class="sub_nav_con_m">
        <div class="sub_nav_con_t">
            <div class="layer p5_0_0_10">
                <ul class="ul_link_03">
                    <li>
                        <a href="/zdal/index.htm?c=100015001" class="a_btn_01">
                            <span class="sp_r">
                                <span class="sp_m">
                                    <span class="sp_arrow">民事参阅案例</span>
                                </span>
                            </span>
                        </a>
                    </li>
                    <li>
                        <a href="/zdal/index.htm?c=100015002"  class="a_btn_01">
                            <span class="sp_r">
                                <span class="sp_m">
                                    <span class="sp_arrow">商事参阅案例</span>
                                </span>
                            </span>
                        </a>
                    </li>
                    <li>
                        <a href="/zdal/index.htm?c=100015003"  class="a_btn_01">
                            <span class="sp_r">
                                <span class="sp_m">
                                    <span class="sp_arrow  grid_layout_135" style="padding-right: 45px">知识产权参阅案例</span>
                                </span>
                            </span>
                        </a>
                    </li>
                    <li>
                        <a href="/zdal/index.htm?c=100015004"  class="a_btn_01">
                            <span class="sp_r">
                                <span class="sp_m">
                                    <span class="sp_arrow">  刑事参阅案例</span>
                                </span>
                            </span>
                        </a>
                    </li>
                    <li>
                        <a href="/zdal/index.htm?c=100015005"  class="a_btn_01">
                            <span class="sp_r">
                                <span class="sp_m">
                                    <span class="sp_arrow">行政参阅案例   </span>
                                </span>
                            </span>
                        </a>
                    </li>
                    <li>
                        <a href="/zdal/index.htm?c=100015006"  class="a_btn_01">
                            <span class="sp_r">
                                <span class="sp_m">
                                    <span class="sp_arrow">执行参阅案例</span>
                                </span>
                            </span>                                                     
                        </a>
                    </li>
                    <li>
                        <a href="/zdal/index.htm?c=100015007"  class="a_btn_01">
                            <span class="sp_r">
                                <span class="sp_m">
                                    <span class="sp_arrow grid_layout_135" style="padding-right: 45px">国家赔偿参阅案例</span>
                                </span>
                            </span>     
                        </a>
                    </li>                               
                </ul>
                <!-- ul_link_03 end -->
            </div>
            <!-- layer end -->
        </div>
        <!-- sub_nav_con_t end -->
    </div>
    <!-- sub_nav_con_m end -->
</div>  
<!-- sub_nav_con end --></li>
                <li class="li_item   "><a href='/ssfw/index.htm'
                    class="a_li_item">诉讼服务</a>
                    <div class="sub_nav_con"  style="display:;">
    <div class="sub_nav_con_m">
        <div class="sub_nav_con_t">
            <div class="layer p5_0_0_10">
                <ul class="ul_link_03">
                    <li>
                        <a href="/ssfw/index.htm" class="a_btn_01">
                            <span class="sp_r">
                                <span class="sp_m">
                                    <span class="sp_arrow">网上立案</span>
                                </span>
                            </span>
                        </a>
                    </li>
                    <li>
                        <a href="/ssfw/ajcx.htm"  class="a_btn_01">
                            <span class="sp_r">
                                <span class="sp_m">
                                    <span class="sp_arrow"> 案件查询</span>
                                </span>
                            </span>
                        </a>
                    </li>
                    <li>
                        <a href="/ssfw/wsyj.htm"  class="a_btn_01">
                            <span class="sp_r">
                                <span class="sp_m">
                                    <span class="sp_arrow"> 网上阅卷</span>
                                </span>
                            </span>
                        </a>
                    </li>
                    <li>
                        <a href="/fyzy/index.htm"  class="a_btn_01">
                            <span class="sp_r">
                                <span class="sp_m">
                                    <span class="sp_arrow  ">法院指引 </span>
                                </span>
                            </span>
                        </a>
                    </li>
                    <li>
                        <a href="/ssfw/sszn.htm"  class="a_btn_01">
                            <span class="sp_r">
                                <span class="sp_m">
                                    <span class="sp_arrow"> 诉讼指南</span>
                                </span>
                            </span>
                        </a>
                    </li>
                    <li>
                        <a href="/ssfw/wsys.htm"  class="a_btn_01">
                            <span class="sp_r">
                                <span class="sp_m">
                                    <span class="sp_arrow">文书样式 </span>
                                </span>
                            </span>
                        </a>
                    </li>
                    <li>
                        <a href="/ssfw/ssgj.htm"  class="a_btn_01">
                            <span class="sp_r">
                                <span class="sp_m">
                                    <span class="sp_arrow">诉讼工具  </span>
                                </span>
                            </span>                                                     
                        </a>
                    </li>                           
                </ul>
                <!-- ul_link_03 end -->
            </div>
            <!-- layer end -->
        </div>
        <!-- sub_nav_con_t end -->
    </div>
    <!-- sub_nav_con_m end -->
</div>  
<!-- sub_nav_con end --></li>
                <li class="li_item   "><a href='/sssp/index.htm'
                    class="a_li_item">数说审判</a>
                     <div class="sub_nav_con"  style="display:;">
    <div class="sub_nav_con_m">
        <div class="sub_nav_con_t">
            <div class="layer p5_0_0_10">
                <ul class="ul_link_03">
                    <li>
                        <a href="/sssp/index.htm?tab=0" class="a_btn_01">
                            <span class="sp_r">
                                <span class="sp_m">
                                    <span class="sp_arrow grid_layout_190">全市各法院全年案件统计</span>
                                </span>
                            </span>
                        </a>
                    </li>
                    <li>
                        <a href="/sssp/index.htm?tab=1"  class="a_btn_01">
                            <span class="sp_r">
                                <span class="sp_m">
                                    <span class="sp_arrow grid_layout_190"> 全市各法院当天案件统计</span>
                                </span>
                            </span>
                        </a>
                    </li>
                    <li>
                        <a href="/sssp/index.htm?tab=2"  class="a_btn_01">
                            <span class="sp_r">
                                <span class="sp_m">
                                    <span class="sp_arrow  grid_layout_190">  全市全年案件分类统计</span>
                                </span>
                            </span>
                        </a>
                    </li>
                    
                    <li>
                        <a href="/sssp/index.htm?tab=3" class="a_btn_01">
                            <span class="sp_r">
                                <span class="sp_m">
                                    <span class="sp_arrow grid_layout_190">全市法院全年公开信息统计</span>
                                </span>
                            </span>
                        </a>
                    </li>
                    <li>
                        <a href="/sssp/index.htm?tab=4"  class="a_btn_01">
                            <span class="sp_r">
                                <span class="sp_m">
                                    <span class="sp_arrow grid_layout_190"> 全市法院全年流程公开统计</span>
                                </span>
                            </span>
                        </a>
                    </li>
                    <li>
                        <a href="/sssp/index.htm?tab=5"  class="a_btn_01">
                            <span class="sp_r">
                                <span class="sp_m">
                                    <span class="sp_arrow  grid_layout_190">  全市法院全年文书统计</span>
                                </span>
                            </span>
                        </a>
                    </li>
                                        
                </ul>
                <!-- ul_link_03 end -->
            </div>
            <!-- layer end -->
        </div>
        <!-- sub_nav_con_t end -->
    </div>
    <!-- sub_nav_con_m end -->
</div>  
<!-- sub_nav_con end --></li>
                <li class="li_item last  "><a href='/tszx/vod.htm?ssssuri=/ssss/index/index.html'
                    class="a_li_item">视说诉讼</a>
                    <div class="sub_nav_con"  style="display:;">
     <div class="sub_nav_con_m">
            <div class="sub_nav_con_t">
                 <div class="layer p5_0_0_10">
                      <ul class="ul_link_03">
                           <li>
                                  <a href="http://www.bjcourt.gov.cn/tszx/vod.htm?ssssuri=/szbyg/index.html" class="a_btn_01">
                                       <span class="sp_r">
                                             <span class="sp_m">
                                                   <span class="sp_arrow">直播预告</span>
                                             </span>
                                       </span>
                                   </a>
                               </li>
                           <li>
                                  <a href="http://www.bjcourt.gov.cn/tszx/vod.htm?ssssuri=/mediaIndex?menuIndex=0" class="a_btn_01">
                                       <span class="sp_r">
                                             <span class="sp_m">
                                                   <span class="sp_arrow">庭审直击</span>
                                             </span>
                                       </span>
                                   </a>
                               </li>
                           <li>
                                  <a href="http://www.bjcourt.gov.cn/tszx/vod.htm?ssssuri=/mediaIndex?menuIndex=8a9681fb4481cfd3014481d0ccb00005&secname=%25E4%25BC%259A%25E8%25AE%25AE%25E7%259B%25B4%25E5%2587%25BB" class="a_btn_01">
                                       <span class="sp_r">
                                             <span class="sp_m">
                                                   <span class="sp_arrow">会议直击</span>
                                             </span>
                                       </span>
                                   </a>
                               </li>
                           <li>
                                  <a href="http://www.bjcourt.gov.cn/tszx/vod.htm?ssssuri=/mediaIndex?menuIndex=8a9681fb4481cfd3014481cfd3f80000&secname=%25E6%25B3%2595%25E5%25AE%2598%25E9%25A3%258E%25E9%2587%2587" class="a_btn_01">
                                       <span class="sp_r">
                                             <span class="sp_m">
                                                   <span class="sp_arrow">法官风采</span>
                                             </span>
                                       </span>
                                   </a>
                               </li>
                           <li>
                                  <a href="http://www.bjcourt.gov.cn/tszx/vod.htm?ssssuri=/mediaIndex?menuIndex=8a9681fb4481cfd3014481d007d90001&secname=%25E6%25B3%2595%25E9%2599%25A2%25E8%25A7%2586%25E8%25AE%25B0" class="a_btn_01">
                                       <span class="sp_r">
                                             <span class="sp_m">
                                                   <span class="sp_arrow">法院视记</span>
                                             </span>
                                       </span>
                                   </a>
                               </li>
                           <li>
                                  <a href="http://www.bjcourt.gov.cn/tszx/vod.htm?ssssuri=/mediaIndex?menuIndex=8a9681fb4481cfd3014481d038300002&secname=%25E6%2599%25AE%25E6%25B3%2595%25E8%25A7%2586%25E7%2582%25B9" class="a_btn_01">
                                       <span class="sp_r">
                                             <span class="sp_m">
                                                   <span class="sp_arrow">普法视点</span>
                                             </span>
                                       </span>
                                   </a>
                               </li>
                           <li>
                                  <a href="http://www.bjcourt.gov.cn/tszx/vod.htm?ssssuri=/mediaIndex?menuIndex=8a9681fb4481cfd3014481d0ccb00004&secname=%25E6%25B3%2595%25E5%2588%25B6%25E8%25A7%2586%25E9%25A2%2591" class="a_btn_01">
                                       <span class="sp_r">
                                             <span class="sp_m">
                                                   <span class="sp_arrow">法制视频</span>
                                             </span>
                                       </span>
                                   </a>
                               </li>
                           <li>
                                  <a href="http://www.bjcourt.gov.cn/tszx/vod.htm?ssssuri=/mediaIndex?menuIndex=8a9681fb4481cfd3014481d0ab8b0003&secname=%25E6%25B3%2595%25E8%258B%2591%25E6%2595%2585%25E8%25A7%2586" class="a_btn_01">
                                       <span class="sp_r">
                                             <span class="sp_m">
                                                   <span class="sp_arrow">法苑故视</span>
                                             </span>
                                       </span>
                                   </a>
                               </li>
                           </ul>
                     <!-- ul_link_03 end -->
               </div>
               <!-- layer end -->
           </div>
           <!-- sub_nav_con_t end -->
     </div>
     <!-- sub_nav_con_m end -->
</div>  
<!-- sub_nav_con end --></li>
            </ul>
        </div>
    </div>
    <!-- header_b end -->
</div>
<!-- header end --><div class="content pt25 pb45">
            <div class="main">
            <div class="sub_page_hd_max">
	<h2 class="h2_pos  fl">
		<a href="/">首页</a><span class="sp_line">-</span><a href="/zxxx/indexOld.htm?zxxxlx=100013001">执行信息</a><span class="sp_line">-</span><span class="sp_curret">限制出境被执行人</span>
</h2>
	<!-- sp_pos end -->
    <div class="search_all_box">
	<div class="search_menu" id="search_menu">
		<div class="search_value_box">
			<span class="sp_gain_value">裁判文书</span>
			<span class="sp_mousedown" style="float: left;" id="sp_mousedown"></span>
		    <input type="hidden" id="searchType1" value="cpws" />
		    <input type="hidden" id="searchCondtion" value="" />
		</div>
		<!-- search_value_box end -->
		<dl class="search_con_nav" id="search_con_nav1">
			<dd value="cpws">裁判文书</dd>
			<dd value="ktgg">开庭公告</dd>
			<dd value="bggs">减刑假释类公示</dd>
			<dd value="other">其他</dd>
			<dd value="totalIndex">全站检索</dd>
		</dl>
		<!-- search_con_nav end -->
	</div>
	<!-- search_menu end -->
	<div class="search_all_wrap">
		<input type="text" name="" id="bg_search" onkeydown="SEARCH.enterGoTo(event);" value="输入关键词搜索"
			class="inp_search_all" onkeypress="entersearch()"/> <a href="javascript:SEARCH.search1();"
			class="search_all_btn"></a>
	</div>
	<!-- search_all_wrap end -->
</div>
<!-- search_all_box end --></div><div class="layer shadow">
                    <h3 class="h3_18_m_blue_bg">
                        <span class="sp_title">限制出境被执行人</span>
                        <span class="sp_r">
                            <a href='/zxxx/indexOld.htm?zxxxlx=100013002' class="a_03"> 返回 </a>
                        </span>
                    </h3>
                </div>
                <!-- layer end -->
                <div class="layer p25_0_10">
	                <table class="table_list_03" >
		                    <tr><td class="td_01">姓名</td><td>李红亮</td></tr>
		                    <tr><td class="td_01">证件类型</td><td>居民身份证</td></tr>
		                    <tr><td class="td_01">证件号码</td><td> 340822198203032413</td></tr>
		                    <tr><td class="td_01">国籍</td><td> </td></tr>
		                    <tr><td class="td_01">性别</td><td>男性</td></tr>
		                    <tr><td class="td_01">案号</td><td>2011年通执字第05093号</td></tr>
		                    <tr><td class="td_01">立案时间</td><td>Aug 15, 2011</td></tr>
		                    <tr><td class="td_01">执行依据文号</td><td>2011年通民初字第04342号</td></tr>
		                    <tr><td class="td_01">执行法院</td><td>北京市通州区人民法院</td></tr>
		                    <tr><td class="td_01 td_01_last">承办法官</td><td class="td_01_last">张金孝</td></tr>
		                </table>
		            </div>
            </div>
            <!-- main end -->
        </div>
        <!-- content end -->
        <div class="footer">
	<div class="footer_in">
		<div class="footer_l">
			<div class="friend_link">
				<span>友情链接 ： </span>
				<a href="http://www.court.gov.cn/" target="_blank">最高人民法院网 </a>
<a href="http://www.court.gov.cn/zgcpwsw/" target="_blank">中国裁判文书网 </a> 
<a href="http://www.chinacourt.org/index.shtml" target="_blank">中国法院网 </a>
<a href="http://www.xinhuanet.com/" target="_blank">新华网</a>
<a href="http://www.people.com.cn/" target="_blank">人民网</a> 
<a href="http://www.gmw.cn/" target="_blank">光明网</a>
<a href="http://www.legaldaily.com.cn/" target="_blank">法制网 </a>
<a href="http://www.jcrb.com/" target="_blank">正义网 </a></div>
			<!-- friend_link end -->
			<div class="copyright" >
			    <span style="width: 340px;float: left;">
				<p>北京市高级人民法院版权所有</p>
<p>地址 ： 北京市朝阳区建国门南大街10号 技术服务</p><p class="p_bh">京ICP备13053290号   京公网安备11010502025090</p>
				</span>
				<span style="width: 150px;float: left;">
				<a href="//bszs.conac.cn/sitename?method=show&amp;id=278959E193AA2E8AE053022819AC391D" target="_blank">
                  <img id="imgConac" vspace="0" hspace="0" border="0" src="//dcs.conac.cn/image/red_error.png" data-bd-imgshare-binded="1">
                 </a>
                 </span>
			</div>
			   <!-- <script type="text/javascript">
                    document.write(
                            unescape("%3Cspan id='_ideConac'%3E3C/span%3E%3Cscript src='http://dcs.conac.cn/js/01/000/0000/60624207/CA010000000606242070003.js' type='text/javascript'%3E%3C/script%3E"));
               </script> -->
			
		</div>
		<!-- footer_l end -->
		<div class="footer_r">
		<div class="fyyz"></div></div>
		<!-- footer_r end -->

	</div>
	<!-- footer_in end -->
</div>
<!-- footer end -->
<script type="text/javascript" src="/pub/blueskin/scripts/addfocus.js"></script>
<script type="text/javascript" src="/pub/blueskin/scripts/addSelect.js"></script>
<script type="text/javascript" src="/pub/blueskin/scripts/global.js"></script>
<script type="text/javascript" src="/pub/blueskin/scripts/search.js"></script>
<script src="/jq/jquery-ui/jquery-ui-1.9.2.custom.min.js"></script>
<script src="/jq/jquery-ui/jquery.ui.datepicker-zh-CN.js"></script>
<script type="text/javascript">
        $(document).ready(function(){
            $(".date_input").datepicker({});
            if(typeof document.body.style.maxHeight=="undefined"){
                $(".sp_login_btn,.sp_count,.a_login ,.a_logo,.header_b,.main_nav .first_item a,.dl_left_nav dt ,.dl_left_nav dd span,.dl_left_nav dd a,.sp_mousedown,.search_all_btn,.shadow").addClass("png_bg");
            }
            //sp_login_btn
            $(".header_info  .sp_login_btn").hover(function(){
                $(this).addClass("sp_login_btn_hover");
            },function (){
                $(this).removeClass("sp_login_btn_hover");  
            });
            
        });
        $("#search_menu").addSelect({
            triggerEleId:"sp_mousedown",
            searchContentContain:".search_con_nav", 
            addHoverClass:"dd_hover",
            getValueClass:".sp_gain_value"
        });
        $("#search_menu_index").addSelect({
            triggerEleId:"sp_mousedown_index",
            searchContentContain:".search_con_nav", 
            addHoverClass:"dd_hover",
            getValueClass:".sp_gain_value"
        });
        $("#bg_search").addFocus({
            textContent : "输入关键词搜索",
            defaultColor : "#ababab",
            textColor : "#333",
            whetherAddClass : false,
            newClass : ""
        });
        
    </script>
<!--[if IE 6]>
    <script src="scripts/DD_belatedPNG_0.0.8a-min.js"></script>
    <script>
        DD_belatedPNG.fix('.png_bg');
    </script>
<![endif]--><div style="position: fixed;top:150px;width:100%; z-index: 999999;display: none;" id="addQRCodeDialog" >
    <div class="qrcode_area">
        <div class="qrcode_header">
             <span>请扫描二维码下载</span>
             <span style="font-size:12px;">（支持android2.3及以上版本，ios版本正在研发，敬请期待）</span>
             <a class="qrcode_close " id="cancelAddQRCodeDialog" ></a>
        </div>
        <div class="qrcode_body">
              <div class="one_qrcode">
                 <p class="qrcode_title">移动诉讼服务</p>
                 <p class="qrcode_content">
                    <img src="/pub/blueskin/images/ewm_ydxx.png"/>                     
                      </p>
                 <p class="qrcode_desc">移动诉讼服务为公众提供了法院要闻、公告发布、诉讼指南、法院导航、诉讼工具等五项服务。</p>
              </div>
              <div class="one_qrcode">
                 <p class="qrcode_title">移动案件查询</p>
                 <p class="qrcode_content">
                   <img src="/pub/blueskin/images/ewm_ydss.png" />
                      </p>
                 <p class="qrcode_desc">移动案件查询为北京法院涉案当事人提供案件进展查询服务，登陆后可及时接收案件进展通知和电子送达文书信息。</p>
              </div>
        </div>
   </div>
</div><script type="text/javascript" src="/pub/blueskin/scripts/layerbox.js"></script>
<script type="text/javascript">
   $(function(){
       layerDialogPage();
       var status = null;
       $(".addQRCodebtn").mouseenter(function(){
          var that = this;
           status = setTimeout(function(){
               $(that).trigger("click");
           }, 1000);
       }).mouseleave(function(){
          clearTimeout(status);
       });
/*        $(".qrcode_area").mouseleave(function(){
           $("#cancelAddQRCodeDialog").trigger("click");
       }); */
   });
</script>
</div>
</body>
</html>
    '''
    ah = BeiJing(path='失信被执行人', list=s, detail=d)
    print(ah.sxbzx())
    pass

