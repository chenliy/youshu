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


class ChongQing(Base):

    def __init__(self,**kwargs):
        super(ChongQing,self).__init__(**kwargs)
        self.html = etree.HTML(self.list)
        self.results = self.html.xpath('//td')
        self.name = self.results[0].xpath('.//text()')[0] if self.results[0].xpath('.//text()') else ''
        self.case_code = self.results[1].xpath('./text()')[0] if self.results[1].xpath('./text()') else ''
        self.court_name = self.results[2].xpath('./text()')[0] if self.results[2].xpath('./text()') else ''

        self.soup = BeautifulSoup(self.detail, 'lxml')
        self.detail_results = self.soup.find('table').get_text().replace('\n\n\n', ';').replace('\n', '') + ';'
        # print(self.detail_results)
        self.sex = re.findall(r'性       别：(.+?);', self.detail_results)[0] if re.findall(r'性       别：(.+?);',
                                                                               self.detail_results) else ''
        self.reg_date = re.findall(r'立案日期：(.+?);', self.detail_results)[0] if re.findall(r'立案日期：(.+?);',
                                                                               self.detail_results) else None
        self.card_num = re.findall(r'身份证号码：(.+?);', self.detail_results)[0] if re.findall(r'身份证号码：(.+?);',
                                                                                self.detail_results) else ''

        self.itype = ''

        self.area_name = '重庆'
        # self.start_date = None
        # self.release_date = None
        self.source = self.path
        pass

    def sxbzx(self):
        print('{}:{}'.format(datetime.now(), self.path))
        self.executive_person['name'] = self.name
        self.executive_person['case_code'] = self.case_code
        self.executive_person['court_name'] = self.court_name
        self.executive_person['sex'] = self.sex
        self.executive_person['reg_date'] = self.reg_date
        self.executive_person['card_num'] = self.card_num
        # self.executive_person['release_date'] = self.release_date
        self.executive_person['area_name'] = self.area_name
        self.executive_person['source'] = self.path
        # print(self.executive_person)
        self.executive_person['operator'] = 'wangfeng'
        # return self.executive_person

    def xzgxf(self):
        print('{}:{}'.format(datetime.now(), self.path))
        # self.exposure_desk["exposure_type"] = self.exposure_type
        self.exposure_desk['name'] = self.name
        self.exposure_desk['itype'] = self.itype
        self.exposure_desk['card_num'] = self.card_num
        self.exposure_desk['case_code'] = self.case_code
        self.exposure_desk['court_name'] = self.court_name
        self.exposure_desk['sex'] = self.sex
        # self.executive_desk['start_date'] = self.start_date
        self.exposure_desk['source'] = self.source
        self.exposure_desk['operator'] = 'wangfeng'

        self.executive_announcement['operator'] = 'wangfeng'
        # print(self.exposure_desk)
        super().split_ex()
        # return self.exposure_desk

    def xzcj(self):
        return self.xzgxf()



if __name__ == '__main__':
    s = '''
       <tr>
       <td><a href="javascript:getGsbgxx('3eac0909-f951-4d33-9a26-aed62e53f58d')">陈秀兰</a> </td>
       <td>(2015)渝北法民执字第03473号 </td>
       <td>重庆市渝北区人民法院 </td>
       </tr>
    '''
    d = '''
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>

<title>公众服务网</title>
<link href="/court/css/ny.css" rel="stylesheet" type="text/css" />
<script src="/court/js/jquery-1.8.0.min.js"></script>
</head>

<body>
<div class="tc_window" style="width:666px; height: 349px;">
  <div class="tc_window_bt"><b></b></div>
        
    <input type="hidden" id="id" name="gsbg.id" value="3eac0909-f951-4d33-9a26-aed62e53f58d" />
    <table class="mytable" width="100%" height="87%">
      <tr>
      <th width="100%" colspan="4"  align="center" class="tc_td01" >案件详细信息</th>
      </tr>
       <tr class="tr_color">
      <td width="18%" align="right" class="acu">案件字号：</td>
      <td width="35%">(2015)渝北法民执字第03473号</td>
      <td width="20%" align="right" class="acu">法&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;院：</td>
      <td width="35%">重庆市渝北区人民法院</td>
      </tr>
       <tr class="tr_color">
      <!--
      <td align="right" class="acu">申请标的：</td>
      <td> 元 </td>
      -->
      <td align="right" class="acu">立案日期：</td>
      <td colspan="3">2015-09-09</td>
      </tr>
      <tr>
      <th width="100%" colspan="4" align="center" class="tc_td01">当事人详细信息</th>
      </tr>
      
       <tr class="tr_color">
      <td align="right" class="acu">姓&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;名：</td>
      <td>陈秀兰</td>
      <td align="right" class="acu">性&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;别：</td>
      
      
      <td>女</td>
      
      </tr>
       <tr class="tr_color">
      <td align="right" class="acu">民&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;族：</td>
      <td></td>
      <td align="right" class="acu">身份证号码：</td>
      
      
      <td>5102131970****4029</td>
      </tr>
      
      
      
      
      
        <tr class="tr_color">
        <td align="right" class="acu">单位名称：</td>
        <td colspan="4"></td>
        </tr>
      
      <!--
      <tr class="tr_color">
       <td align="right" class="acu">立案部门：</td>
      <td></td>
      <td align="right" class="acu">标的额：</td>
      <td></td>
      </tr>
      <tr class="tr_color">
       <td  align="right" class="acu">应缴案件受理费：</td>
      <td></td>
      <td  align="right" class="acu">承办部门：</td>
      <td></td>
      </tr>
       <tr class="tr_color">
      <td width="100%" colspan="4"  bgcolor="#DFD2C4" align="center" class="acu">结案信息</td>
      </tr>
       <tr class="tr_color">
      <td  align="right" class="acu">结案日期：</td>
      <td></td>
      <td  align="right" class="acu">结案案由：</td>
      <td></td>
      </tr>
       <tr class="tr_color">
       <td  align="right" class="acu">结案方式：</td>
      <td></td>
      <td  align="right" class="acu">宣判日期：</td>
      <td></td>
      </tr>
       <tr class="tr_color">
      <td width="100%" colspan="4"  bgcolor="#DFD2C4" align="center" class="acu">归档信息</td>
      </tr>
       <tr class="tr_color">
       <td  align="right" class="acu">归档日期：</td>
      <td></td>
      <td  align="right" class="acu">移交卷宗日期：</td>
      <td></td>
      </tr>
      
          <tr>
      <td colspan="4" style="border-bottom: 0px;border-bottom-width: 0">
        浏览次数: <span id="count"></span> 次      
      </td>
      </tr>-->
      <tr>
      <td colspan="4" style="border-bottom: 0px;border-bottom-width: 0" align="center">
        <a class="s_2" href="###" onclick="top.closeDialog();" style="margin-left:250px;">关闭</a>
        <a class="s_1" href="###" onclick="tozxxsjb('','陈秀兰','(2015)渝北法民执字第03473号','重庆市渝北区人民法院');" style="margin-left:20px;">线索举报</a>     
      </td>
      </tr>
         </table>
    
             
  </div>
</body>

<script type="text/javascript">
$(function(){
  //getViewcount();
});
//获取统计信息
function getViewcount(){
  var id = $("#id").val();
  var url = "/court/gg_listviewcountGsbg.shtml?id="+id;
  var params = {
  };
  $.post(url,params,function(data){
    var obj = eval("["+data+"]");
    if(obj!=null){
      var count = obj[0].count;
      $("#count").empty().append(count);
    }
  }); 
}
//跳转线索举报
function tozxxsjb(fydm,xm,ahqc,fymc){
  var url = "/court/user_isLogin.shtml";
  $.post(url,{},function(data){
    if(data!=null&&data=="true"){
      top.self.location.href='/court/ccxs_ccxsjbxx.shtml?fydm='+fydm+'&xm='+encodeURI(encodeURI(xm))+'&ahqc='+encodeURI(encodeURI(ahqc))+'&fymc='+encodeURI(encodeURI(fymc));
      return false;
    }else{
      alert("请先进行登陆！");
      top.toLogin();
      return false;
    }
  });
}

</script>
</html>
    '''
    ah = ChongQing(path='失信被执行人', list=s, detail=d)
    print(ah.sxbzx())
    pass

