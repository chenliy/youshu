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

class LiaoNing(Base):

    def __init__(self,**kwargs):
        super(LiaoNing,self).__init__(**kwargs)
        self.html = etree.HTML(self.list)
        self.results = self.html.xpath('//td')
        self.name = self.results[1].xpath('./div/text()')[0] if self.results[1].xpath('.//text()') else ''
        self.case_code = self.results[2].xpath('./div/text()')[0] if self.results[2].xpath('./text()') else ''
        self.card_num = self.results[3].xpath('./div/text()')[0] if self.results[3].xpath('./text()') else ''

        self.soup = BeautifulSoup(self.detail, 'lxml')
        self.detail_results = self.soup.find('table',{'class':'fd_table_02'}).get_text().replace('\n\n\n\n', ';').replace('\n\n', '：') + ';'
        # print(self.detail_results)

        self.identity = re.findall(r'诉讼地位：(.+?);', self.detail_results)[0].strip() if re.findall(r'诉讼地位：(.+?);', self.detail_results) else ''
        self.itype = re.findall(r'类型：(.+?);', self.detail_results)[0].strip() if re.findall(r'类型：(.+?);', self.detail_results) else ''

        self.sex = re.findall(r'性别：(.+?);', self.detail_results)[0].strip() if re.findall(r'性别：(.+?);', self.detail_results) else ''
        self.age = re.findall(r'年龄：(.+?);', self.detail_results)[0].strip() if re.findall(r'年龄：(.+?);', self.detail_results) else ''
        self.reg_date = re.findall(r'立案日期：(.+?);', self.detail_results)[0].strip() if re.findall(r'立案日期：(.+?);',
                                                                               self.detail_results) else None
        self.court_name = re.findall(r'执行法院：(.+?);', self.detail_results)[0].strip() if re.findall(r'执行法院：(.+?);',
                                                                               self.detail_results) else ''
        self.case_status = re.findall(r'案件状态：(.+?);', self.detail_results)[0].strip() if re.findall(r'案件状态：(.+?);',
                                                                                  self.detail_results) else ''
        self.execute_money = re.findall(r'申请执行标的金额：(.+?);', self.detail_results)[0].strip() if re.findall(r'申请执行标的金额：(.+?);',
                                                                                        self.detail_results) else ''
        self.gist_id = re.findall(r'编号：(.+?);', self.detail_results)[0].strip() if re.findall(r'号：(.+?);',
                                                                                        self.detail_results) else ''
        self.gist_unit = re.findall(r'经办机构（做出执行依据单位）：(.+?);', self.detail_results)[0].strip() if re.findall(r'经办机构（做出执行依据单位）：(.+?);',
                                                                                        self.detail_results) else ''
        self.release_date = re.findall(r'发布日期：(.+?);', self.detail_results)[0].strip() if re.findall(r'发布日期：(.+?);',
                                                                                   self.detail_results) else None

        self.performance = re.findall(r'履行情况：(.+?);', self.detail_results)[0].strip() if re.findall(r'履行情况：(.+?);',
                                                                                   self.detail_results) else ''
        self.performed_part = re.findall(r'已履行：(.+?);', self.detail_results)[0].strip() if re.findall(r'已履行：(.+?);',
                                                                                   self.detail_results) else ''
        self.unperform_part = re.findall(r'未履行：(.+?);', self.detail_results)[0].strip() if re.findall(r'未履行：(.+?);',
                                                                                   self.detail_results) else ''
        self.duty = re.findall(r'义务：(.+?);', self.detail_results)[0].strip() if re.findall(r'义务：(.+?);',
                                                                                   self.detail_results) else ''
        self.disrupt_type_name = re.findall(r'情形：(.+?);', self.detail_results)[0].strip() if re.findall(r'情形：(.+?);',
                                                                                   self.detail_results) else ''



        self.limiting_cause = re.findall(r'限制原因：(.+?);', self.detail_results)[0].strip() if re.findall(r'限制原因：(.+?);',
                                                                                  self.detail_results) else ''
        self.restricted_content = re.findall(r'限制内容：(.+?);', self.detail_results)[0].strip() if re.findall(r'限制内容：(.+?);', self.detail_results) else ''
        self.start_date = re.findall(r'开始日期：(.+?);', self.detail_results)[0].strip() if re.findall(r'开始日期：(.+?);', self.detail_results) else None
        self.business_entity = re.findall(r'法定代表人姓名：(.+?);', self.detail_results)[0] if re.findall(r'法定代表人姓名：(.+?);',
                                                                                   self.detail_results) else ''
        
        self.area_name = '辽宁'
        self.source = self.path
        pass

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
        self.executive_person['performance'] = self.performance
        self.executive_person['performed_part'] = self.performed_part
        self.executive_person['unperform_part'] = self.unperform_part
        self.executive_person['disrupt_type_name'] = self.disrupt_type_name
        self.executive_person['publish_date'] = self.release_date
        self.executive_person['area_name'] = self.area_name
        self.executive_person['business_entity'] = self.business_entity
        self.executive_person['source'] = self.path
        # print(self.executive_person)
        self.executive_person['operator'] = 'wangfeng'
        # return self.executive_person

    def wjzxssaj(self):
        print('{}:{}'.format(datetime.now(), self.path))
        # self.exposure_desk["exposure_type"] = self.exposure_type
        self.exposure_desk['name'] = self.name
        self.exposure_desk['identity'] = self.identity
        self.exposure_desk['itype'] = self.itype
        self.exposure_desk['age'] = self.age
        self.exposure_desk['sex'] = self.sex
        self.exposure_desk['card_num'] = self.card_num
        self.exposure_desk['case_code'] = self.case_code
        self.exposure_desk['court_name'] = self.court_name
        self.exposure_desk['limiting_cause'] = self.limiting_cause
        self.exposure_desk['restricted_content'] = self.restricted_content
        self.exposure_desk['start_date'] = self.start_date
        self.exposure_desk['reg_date'] = self.reg_date
        self.exposure_desk['release_date'] = self.release_date
        self.exposure_desk['case_status'] = self.case_status
        self.exposure_desk['gist_id'] = self.gist_id
        self.exposure_desk['gist_unit'] = self.gist_unit
        self.exposure_desk['business_entity'] = self.business_entity
        self.exposure_desk['source'] = self.source
        self.exposure_desk['operator'] = 'wangfeng'
        self.executive_announcement['operator'] = 'wangfeng'
        # print(self.exposure_desk)
        super().split_ex()
        # return self.exposure_desk
        pass

    def xzgxf(self):
        return self.wjzxssaj()
        

    def xzcj(self):
        return self.wjzxssaj()

    def xztzb(self):
        return self.wjzxssaj()



if __name__ == '__main__':
    s = '''
       <tr>
       <td class="td_data_row td_data_num" onclick="javascript:zxsxDetail('2E65C4CBBCF7AF2C3B4AC414DC2F0600');">
       <div class="td_cell">2</div>
       </td>
       <td class="td_data_row " onclick="javascript:zxsxDetail('2E65C4CBBCF7AF2C3B4AC414DC2F0600');">
       <div class="td_cell">钱本海</div>
       </td>
       <td class="td_data_row " onclick="javascript:zxsxDetail('2E65C4CBBCF7AF2C3B4AC414DC2F0600');">
       <div class="td_cell">（2016）辽12执103号</div>
       </td>
       <td class="td_data_row " onclick="javascript:zxsxDetail('2E65C4CBBCF7AF2C3B4AC414DC2F0600');">
       <div class="td_cell">2112021967+***0031</div>
       </td>
       <td class="td_data_row " onclick="javascript:zxsxDetail('2E65C4CBBCF7AF2C3B4AC414DC2F0600');">
       <div class="td_cell">限制出境</div>
       </td>
       <td class="td_data_row ">
       </td>
       </tr>
    '''
    d = '''
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta charset="UTF-8">
    <title>被执行人钱本海详情-被执行人查询-诉讼无忧网</title>
    <script type="text/javascript">
  var contextPath = "/susong51";
  var theSessionId = "22313D454812B906A364273CD41E734A.sswy2";
</script>
<link rel="stylesheet" type="text/css" href="/susong51/jq/alerts/jquery.alerts.css">
<link charset="utf-8" rel="stylesheet" type="text/css" href="/susong51/pub/V3/css/import.css" media="all" />
<link charset="utf-8" rel="stylesheet" type="text/css" href="/susong51/pub/V3/css/variable_blue.css" media="all" />
<!--[if IE]>
    <script type="text/javascript" src="/susong51/pub/V3/scripts/html5.js"></script>
<![endif]--> 
<script type="text/javascript" src="/susong51/jq/jquery-1.8.3.js"></script>
<script type="text/javascript" src="/susong51/common/js/handlebars-v4.0.5.js"></script>
<script type="text/javascript" src="/susong51/jq/alerts/jquery.alerts.js"></script>
<script type="text/javascript" src="/susong51/jq/jquery.json-2.4.js"></script>
<script type="text/javascript" src="/susong51/jq/jquery.form.js"></script>
<script type="text/javascript" src="/susong51/pub/comm.js"></script>
<script type="text/javascript" src="/susong51/pub/V3/scripts/global.js"></script>
<script type="text/javascript" src="/susong51/pub/lsfwpt/js/global.js"></script>
<script type="text/javascript" src="/susong51/pub/V3/scripts/bootstrap-modal.js"></script>
<script type="text/javascript">
  $.ajaxSetup({
    contentType : "application/x-www-form-urlencoded;charset=utf-8",
    complete : function(XMLHttpRequest, textStatus){
      var sessionstatus = XMLHttpRequest.getResponseHeader("sessionstatus"); 
      if(sessionstatus == "timeout"){
        var loginUrl = XMLHttpRequest.getResponseHeader("loginUrl");
        if (SSWY.isEmpty(loginUrl)) {
          loginUrl = contextPath + "/login/pro.htm";
        } else {
          loginUrl = contextPath + loginUrl;
        }
        window.location.replace(loginUrl);
      }
    }
  });
  $.fn.pasteEvents = function( delay ) {
      if (delay == undefined) delay = 20;
      return $(this).each(function() {
          var $el = $(this);
          $el.on("paste", function() {
              $el.trigger("prepaste");
              setTimeout(function() { $el.trigger("postpaste"); }, delay);
          });
      });
  };
  
  $.fn.setCursorPosition = function(option) {
      var settings = $.extend({
          index: 0
      }, option)
      return this.each(function() {
          var elem  = this
          var val   = elem.value
          var len   = val.length
          var index = settings.index
   
          // éinputåtextareaç´æ¥è¿å
          var $elem = $(elem)
          if (!$elem.is('input,textarea')) return
          // è¶è¿ææ¬é¿åº¦ç´æ¥è¿å
          if (len < index) return
   
          setTimeout(function() {
              elem.focus()
              if (elem.setSelectionRange) { // æ åæµè§å¨
                  elem.setSelectionRange(index, index)   
              } else { // IE9-
                  var range = elem.createTextRange()
                  range.moveStart("character", -len)
                  range.moveEnd("character", -len)
                  range.moveStart("character", index)
                  range.moveEnd("character", 0)
                  range.select()
              }
          }, 10)
      })
  }
  
</script>
    <script type="text/javascript">
    var courtId = '600';
    var bzxrid = '2E65C4CBBCF7AF2C3B4AC414DC2F0600';
    var fyid = '600';
    function xsjb(){
        var url = contextPath + "/pub/zxxsjb/jbxz.htm?bzxrid=" + bzxrid + "&fy=" + courtId;
        window.open(url);
    };
    </script>
</head>
<body>
<div class="contain fd_contain_noimg">
    <header class="header">
  <div class="header_shadow">
    <div class="header_in">
      















<div class="header_t_bg">
<div class="header_t">
  <a href="http://www.lnsfy.gov.cn" title="辽宁高院审判信息网">返回网站首页</a>
  
    
      <span class="sp_load_prev">
    
    
        <a href="/susong51/login/pro.htm?fy=600" class="a_load">登录</a>
    

    
        <a href="/susong51/login/register.htm?fy=600" class="a_register">注册</a>
    

      </span>
    
    
  
</div>
</div><div class="header_m">
    <a href="http://www.lnsfy.gov.cn" title="辽宁高院审判信息网" class="logo"><img src="/susong51/pub/V3/images/logo.png" alt="logo" />辽宁高院审判信息网</a>
</div>
</div>
  </div>
</header>
  <div class="fd_m_auto fd_width_1000"><h2 class="fd_h2_bnav"><a href="http://www.lnsfy.gov.cn">首页</a><span class="fd_separate">></span><a href="/susong51/fymh/600/zxgk.htm">执行公开</a><span class="fd_separate">></span><span class="current_location">详情</span></h2></div>

    <article class="content">
        <div class="main">
            
                
                    <dl class="dl_01 dl_01_no_shadow dl_01_no_bd dl_01_no_bg">
                        <dt class="dt_hd dt_have_bd">
                            <span class="sp_title">限制出境</span>
                            
                        </dt>
                        <dd class="dd_con">
                            <table class="fd_table_02">
                                
                                <tr class="tr_first" >
                                    <td class="td_data_row td_data_first fd_width_fix_250"><div class="td_cell">诉讼地位</div></td>
                                    <td class="td_data_row td_data_last"><div class="td_cell">
                                        被执行人</div>
                                    </td>
                                </tr>
                                
                                <tr  >
                                    <td class="td_data_row td_data_first "><div class="td_cell">被执行人姓名/名称</div></td>
                                    <td class="td_data_row td_data_last"><div class="td_cell">
                                        钱本海</div>
                                    </td>
                                </tr>
                                
                                <tr  >
                                    <td class="td_data_row td_data_first "><div class="td_cell">被执行人类型</div></td>
                                    <td class="td_data_row td_data_last"><div class="td_cell">
                                        自然人</div>
                                    </td>
                                </tr>
                                
                                <tr  >
                                    <td class="td_data_row td_data_first "><div class="td_cell">证件类型</div></td>
                                    <td class="td_data_row td_data_last"><div class="td_cell">
                                        中华人民共和国居民身份证</div>
                                    </td>
                                </tr>
                                
                                <tr  >
                                    <td class="td_data_row td_data_first "><div class="td_cell">证件号码</div></td>
                                    <td class="td_data_row td_data_last"><div class="td_cell">
                                        2112021967****0031</div>
                                    </td>
                                </tr>
                                
                                <tr  >
                                    <td class="td_data_row td_data_first "><div class="td_cell">被执行人性别</div></td>
                                    <td class="td_data_row td_data_last"><div class="td_cell">
                                        男</div>
                                    </td>
                                </tr>
                                
                                <tr  >
                                    <td class="td_data_row td_data_first "><div class="td_cell">被执行人年龄</div></td>
                                    <td class="td_data_row td_data_last"><div class="td_cell">
                                        49</div>
                                    </td>
                                </tr>
                                
                                <tr  >
                                    <td class="td_data_row td_data_first "><div class="td_cell">限制原因</div></td>
                                    <td class="td_data_row td_data_last"><div class="td_cell">
                                        未履行裁判文书确定义务</div>
                                    </td>
                                </tr>
                                
                                <tr  >
                                    <td class="td_data_row td_data_first "><div class="td_cell">限制内容</div></td>
                                    <td class="td_data_row td_data_last"><div class="td_cell">
                                        限制出境</div>
                                    </td>
                                </tr>
                                
                                <tr  >
                                    <td class="td_data_row td_data_first "><div class="td_cell">限制开始日期</div></td>
                                    <td class="td_data_row td_data_last"><div class="td_cell">
                                        2017-07-10</div>
                                    </td>
                                </tr>
                                
                                <tr  >
                                    <td class="td_data_row td_data_first "><div class="td_cell">案号</div></td>
                                    <td class="td_data_row td_data_last"><div class="td_cell">
                                        （2016）辽12执103号</div>
                                    </td>
                                </tr>
                                
                                <tr  >
                                    <td class="td_data_row td_data_first "><div class="td_cell">立案日期</div></td>
                                    <td class="td_data_row td_data_last"><div class="td_cell">
                                        2016-12-05</div>
                                    </td>
                                </tr>
                                
                                <tr  >
                                    <td class="td_data_row td_data_first "><div class="td_cell">执行法院</div></td>
                                    <td class="td_data_row td_data_last"><div class="td_cell">
                                        铁岭市中级人民法院</div>
                                    </td>
                                </tr>
                                
                                <tr  >
                                    <td class="td_data_row td_data_first "><div class="td_cell">案件状态</div></td>
                                    <td class="td_data_row td_data_last"><div class="td_cell">
                                        审理</div>
                                    </td>
                                </tr>
                                
                                <tr  >
                                    <td class="td_data_row td_data_first "><div class="td_cell">执行依据文书编号</div></td>
                                    <td class="td_data_row td_data_last"><div class="td_cell">
                                        （2016）辽民终227号</div>
                                    </td>
                                </tr>
                                
                                <tr  >
                                    <td class="td_data_row td_data_first "><div class="td_cell">经办机构（做出执行依据单位）</div></td>
                                    <td class="td_data_row td_data_last"><div class="td_cell">
                                        辽宁省高级人民法院</div>
                                    </td>
                                </tr>
                                
                                <tr  >
                                    <td class="td_data_row td_data_first "><div class="td_cell">发布日期</div></td>
                                    <td class="td_data_row td_data_last"><div class="td_cell">
                                        2017-07-04</div>
                                    </td>
                                </tr>
                                
                            </table>
                            <!-- fd_table_02 end -->
                        </dd>
                    </dl>
                
                
            
        </div>
        <!-- main end -->
    </article>
    <!-- content end -->
    <footer class="footer">
  <div class="footer_in">技术支持：北京华宇信息技术有限公司</div>
</footer>
</div>
</body>
</html>
    '''
    ln = LiaoNing(path='失信被执行人', list=s, detail=d)
    print(ln.sxbzx())
    pass

