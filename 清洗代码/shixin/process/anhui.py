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


class AnHui(Base):
    def __init__(self, **kwargs):
        super(AnHui, self).__init__(**kwargs)
        # 初始化数据
        self.name = ''
        self.card_num = ''
        self.court_name = ''
        self.case_code = ''
        self.identity = ''
        self.itype = ''
        self.sex = ''
        self.age = ''
        self.reg_date = ''
        self.trial_round = ''
        self.reason = ''
        self.case_status = ''
        self.execute_money = ''
        self.release_date = ''
        self.duty = ''
        self.disrupt_type_name = ''
        self.business_entity = ''
        self.html = etree.HTML(self.list)
        self.results = self.html.xpath('//td')
        self.name = self.results[1].xpath('./text()')[0] if self.results[1].xpath('./text()') else ''
        self.card_num = self.results[2].xpath('./text()')[0] if self.results[2].xpath('./text()') else ''
        self.court_name = self.results[5].xpath('./text()')[0] if self.results[5].xpath('./text()') else ''
        self.case_code = self.results[4].xpath('./text()')[0] if self.results[4].xpath('./text()') else ''

        # self.soup = ''
        self.area_name = '安徽'
        # self.start_date = None
        self.source = self.path

        self.deal_detail(self.detail)

        print('haha')

    def deal_detail(self, detail):
        self.soup = BeautifulSoup(detail, 'lxml')
        try:
            self.detail_results = self.soup.find('table').get_text().replace('\n\n\n', ';').replace('\n', '') + ';'
            # print(self.detail_results)
            self.identity = re.findall(r'诉讼地位：(.*?);', self.detail_results)[0] if re.findall(r'诉讼地位：(.*?);',
                                                                                             self.detail_results) else ''
            self.itype = re.findall(r'类型：(.*?);', self.detail_results)[0] if re.findall(r'类型：(.*?);',
                                                                                        self.detail_results) else ''

            self.sex = re.findall(r'性别：(.+?);', self.detail_results)[0] if re.findall(r'性别：(.+?);',
                                                                                      self.detail_results) else ''
            self.age = re.findall(r'年龄：(.+?);', self.detail_results)[0] if re.findall(r'年龄：(.+?);',
                                                                                      self.detail_results) else ''
            self.reg_date = re.findall(r'立案日期：(.+?);', self.detail_results)[0] if re.findall(r'立案日期：(.+?);',
                                                                                             self.detail_results) else None
            self.trial_round = re.findall(r'执行程序：(.+?);', self.detail_results)[0] if re.findall(r'执行程序：(.+?);',
                                                                                                self.detail_results) else ''
            self.reason = re.findall(r'执行案由：(.+?);', self.detail_results)[0] if re.findall(r'执行案由：(.+?);',
                                                                                           self.detail_results) else ''
            self.case_status = re.findall(r'案件状态：(.+?);', self.detail_results)[0] if re.findall(r'案件状态：(.+?);',
                                                                                                self.detail_results) else ''
            self.execute_money = re.findall(r'申请执行标的金额：(.+?);', self.detail_results)[0] if re.findall(
                r'申请执行标的金额：(.+?);',
                self.detail_results) else ''
            self.release_date = re.findall(r'发布日期：(.+?);', self.detail_results)[0] if re.findall(r'发布日期：(.+?);',
                                                                                                 self.detail_results) else None
            self.duty = re.findall(r'义务：(.+?);', self.detail_results)[0] if re.findall(r'义务：(.+?);',
                                                                                       self.detail_results) else ''
            self.disrupt_type_name = re.findall(r'情形：(.+?);', self.detail_results)[0] if re.findall(r'情形：(.+?);',
                                                                                                    self.detail_results) else ''
            self.business_entity = re.findall(r'法定代表人姓名：(.+?);', self.detail_results)[0] if re.findall(
                r'法定代表人姓名：(.+?);',
                self.detail_results) else ''
        except Exception as e:
            print(e)

        pass

    def sxbzx(self):
        print('{}:{}'.format(datetime.now(), self.path))
        self.executive_person['name'] = self.name
        self.executive_person['card_num'] = self.card_num
        self.executive_person['court_name'] = self.court_name
        self.executive_person['case_code'] = self.case_code
        self.executive_person['business_entity'] = self.business_entity

        self.executive_person['sex'] = self.sex
        self.executive_person['age'] = self.age
        self.executive_person['reg_date'] = self.reg_date
        self.executive_person['duty'] = self.duty
        self.executive_person['disrupt_type_name'] = self.disrupt_type_name
        self.executive_person['publish_date'] = self.release_date
        self.executive_person['area_name'] = self.area_name
        self.executive_person['source'] = self.path
        self.executive_person['operator'] = 'wangfeng'
        # print(self.executive_person)

    def wjzxssaj(self):
        print('{}:{}'.format(datetime.now(), self.path))
        # 安徽的曝光类型的详情‘对不起，案件所属法院暂未公开案件信息’.
        # self.exposure_desk["exposure_type"] = self.exposure_type
        self.exposure_desk['name'] = self.name
        self.exposure_desk['itype'] = self.itype
        self.exposure_desk['card_num'] = self.card_num
        self.exposure_desk['case_code'] = self.case_code
        self.exposure_desk['court_name'] = self.court_name
        self.exposure_desk['identity'] = self.identity
        self.exposure_desk['sex'] = self.sex
        self.exposure_desk['age'] = self.age
        self.exposure_desk['reg_date'] = self.reg_date
        self.exposure_desk['trial_round'] = self.trial_round
        self.exposure_desk['reason'] = self.reason
        self.exposure_desk['case_status'] = self.case_status
        self.exposure_desk['execute_money'] = self.execute_money
        self.exposure_desk['release_date'] = self.release_date
        self.exposure_desk['business_entity'] = self.business_entity
        # self.exposure_desk['start_date'] = self.start_date
        self.exposure_desk['source'] = self.source
        self.exposure_desk['operator'] = 'wangfeng'

        self.executive_announcement['operator'] = 'wangfeng'
        # print(self.exposure_desk)
        super().split_ex()

    def xzgxf(self):
        return self.wjzxssaj()

    def xzcj(self):
        return self.wjzxssaj()

    def xztzb(self):
        return self.wjzxssaj()


if __name__ == '__main__':
    s = '''
        <tr onclick="javascript:zxsxDetail('059F776EAED8E3845604817A50AA6FEB');">
        <td>6058</td>
        <td>孔维圣</td>
        <td>342622196702063670</td>
        <td>失信人</td>
        <td>(2015)瑶执字第02181号</td>
        <td>合肥市瑶海区人民法院</td>
        </tr>
    '''
    d = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <title>被执行人信息</title>
  <script type="text/javascript">
  var contextPath = "/ssfw";
</script>
<link rel="stylesheet" type="text/css" href="/ssfw/jq/alerts/jquery.alerts.css">
<link charset="utf-8" rel="stylesheet" href="/ssfw/pub/css/min.css" />
<script type="text/javascript" src="/ssfw/jq/jquery-1.8.3.js"></script>
<script type="text/javascript" src="/ssfw/jq/jquery.jqprint-0.3.js"></script>
<script type="text/javascript" src="/ssfw/jq/alerts/jquery.alerts.js"></script>
<script type="text/javascript" src="/ssfw/jq/jquery.json-2.4.js"></script>
<script type="text/javascript" src="/ssfw/jq/jquery.form.js"></script>
<script type="text/javascript" src="/ssfw/pub/comm.js"></script>
<script type="text/javascript" src="/ssfw/pub/js/common.js"></script>
<script type="text/javascript">
  //å¨å±çajaxè®¾ç½®ï¼å¤çajaxæ¸æ±æ¶sesionè¶æ¶
  $.ajaxSetup({
    contentType : "application/x-www-form-urlencoded;charset=utf-8",
    complete : function(XMLHttpRequest, textStatus){
      var sessionstatus = XMLHttpRequest.getResponseHeader("sessionstatus"); //éè¿XMLHttpRequeståå¾ååºå¤´sessionstatus
      if(sessionstatus == "timeout"){
        var loginUrl = XMLHttpRequest.getResponseHeader("loginUrl");
        if (SSWY.isEmpty(loginUrl)) {
          loginUrl = contextPath + "/login/pro.htm";
        } else {
          loginUrl = contextPath + loginUrl;
        }
        window.location.replace(loginUrl); //å¦æè¶æ¶å°±å¤ç ï¼æå®è¦è·³è½¬çé¡µé¢
      }
    }
  });

  //å±è½ä¸ææ¡çéæ ¼é®æä½
  $(document).keydown( function(e) {
      var ev = e || window.event;// è·åeventå¯¹è±¡
      var obj = ev.target || ev.srcElement;// è·åäºä»¶æº
      var t = obj.type || obj.getAttribute('type');// è·åäºä»¶æºç±»å
      // è·åä½ä¸ºå¤æ­æ¡ä»¶çäºä»¶ç±»å
      var vReadOnly = obj.readOnly;
      var vDisabled = obj.disabled;
      // å¤çundefinedå¼æåµ
      vReadOnly = (vReadOnly == undefined) ? false : vReadOnly;
      vDisabled = (vDisabled == undefined) ? false : vDisabled;
      // å½æ²Backspaceé®æ¶ï¼äºä»¶æºç±»åä¸ºå¯ç æåè¡ãå¤è¡ææ¬çï¼
      // å¹¶ä¸readOnlyå±æ§ä¸ºtrueædisabledå±æ§ä¸ºtrueçï¼åéæ ¼é®å¤±æ
      var flag1 = (ev.keyCode == 8)
          && (t == "password" || t == "text" || t == "textarea")
          && (vReadOnly == true || vDisabled == true);
      // å½æ²Backspaceé®æ¶ï¼äºä»¶æºç±»åéå¯ç æåè¡ãå¤è¡ææ¬çï¼åéæ ¼é®å¤±æ
      var flag2 = (ev.keyCode == 8) && (t != "password") && (t != "text")
          && (t != "textarea");
      // å¤æ­
      if (flag2 || flag1) {
        return false;
      }

  });
</script>
  <link rel="stylesheet" type="text/css" href="/ssfw/pub/zxgk/css/reset.css" media="all" />
  <link rel="stylesheet" type="text/css" href="/ssfw/pub/zxgk/css/common.css" media="all" />
  <link rel="stylesheet" type="text/css" href="/ssfw/pub/zxgk/css/global.css" media="all" />
</head>
<body>
  <div class="x_bj">
    <div class="x_top">
      <div class="x_top_in">
        <div class="x_logo">
          <a href="/ssfw/" title="诉讼服务在线平台">诉讼服务在线平台</a>
          <span>被执行人信息</span>
        </div>
        <div class="x_login_box">


              <span>欢迎光临，请</span>
              <a href="/ssfw/login/pro.htm?fy=&url=">[登录]</a>
              <a href="/ssfw/login/register.htm?fy=">[注册]</a>



          <a href="/ssfw/">[返回首页]</a>
        </div>
      </div>
    </div>
    <!-- x_top end -->
    <div class="x_mid">
      <div class="x_main">
        <div class="d_box_01">
          <div align="center">
            <a href="javascript: location.href = document.referrer;">[返回上一页]</a>
          </div>


              <table class="table_01 table_02">
                <tr>
                  <th colspan=2>未结执行实施案件</th>
                </tr>


                  <tr>
                    <td class="bq">诉讼地位：</td>
                    <td>被执行人</td>
                  </tr>



                  <tr>
                    <td class="bq">被执行人姓名/名称：</td>
                    <td>安徽含山东宇机制瓦科技有限公司</td>
                  </tr>



                  <tr>
                    <td class="bq">被执行人类型：</td>
                    <td>法人</td>
                  </tr>



                  <tr>
                    <td class="bq">组织机构代码：</td>
                    <td>74089111-X</td>
                  </tr>



                  <tr>
                    <td class="bq">法定代表人姓名：</td>
                    <td>敬元祥</td>
                  </tr>





                  <tr>
                    <td class="bq">案号：</td>
                    <td>(2016)皖0522执115号</td>
                  </tr>



                  <tr>
                    <td class="bq">立案日期：</td>
                    <td>2016-02-25</td>
                  </tr>



                  <tr>
                    <td class="bq">执行法院：</td>
                    <td>含山县人民法院</td>
                  </tr>



                  <tr>
                    <td class="bq">执行程序：</td>
                    <td>普通执行</td>
                  </tr>



                  <tr>
                    <td class="bq">执行案由：</td>
                    <td>合同、无因管理、不当得利</td>
                  </tr>



                  <tr>
                    <td class="bq">案件状态：</td>
                    <td>审理</td>
                  </tr>



                  <tr>
                    <td class="bq">申请执行标的金额：</td>
                    <td>3518130.00元</td>
                  </tr>







                  <tr>
                    <td class="bq">发布日期：</td>
                    <td>2016-12-24</td>
                  </tr>


              </table>



        </div>
      </div>
      <!-- x_main end -->
    </div>
    <!-- x_mid  end -->
    <div class="x_foot">
      <div class="x_foot_in">
        <p>技术支持：北京华宇信息技术有限公司</p>
      </div>
      <!-- x_foot_in end -->
    </div>
    <!-- x_foot  end -->
  </div>
</body>
</html>

    '''
    ah = AnHui(path='失信被执行人', list=s, detail=d)
    print(ah.sxbzx())
    pass

