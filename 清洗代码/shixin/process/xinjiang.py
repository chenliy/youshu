import os
import sys

from IKEA.shixin.process.guangxi import GuangXi

sys.path.append(os.path.abspath(__file__ + "/../../../../"))
from IKEA.shixin.process.base_process import Base
from IKEA.mysql.mysqlbase import MysqlBase
from IKEA.shixin.config import connecter
from pyquery import PyQuery as pq
from datetime import datetime

class Xinjiang(Base):
    def sxbzx(self):  # 失信被执行
        print('{}:{}'.format(datetime.now(), self.path))
        d = pq(self.detail)
        l = pq(self.list)
        l_list = [each.text() for each in l(".td_cell").items()]
        l_list = l_list[1:4] if len(l_list) > 4 else ['', '', '']
        key_msg = [each.text() for n, each in enumerate(d(".td_cell").items()) if n % 2 == 0]
        value_msg = [each.text() for n, each in enumerate(d(".td_cell").items()) if n % 2 != 0]
        msg = dict(zip(key_msg, value_msg))
        msg = msg if msg else {'被执行人姓名': l_list[0], '执行案号': l_list[1], '身份证号码': l_list[2]}
        self.executive_person['name'] = msg.get('被执行人姓名') if msg.get('被执行人姓名') else msg.get('名称')
        self.executive_person['age'] = msg.get('年龄')
        self.executive_person['card_num'] = msg.get('身份证号码') if msg.get('身份证号码') else msg.get('组织机构代码')
        self.executive_person['performance'] = msg.get('被执行人履行情况')
        self.executive_person['disrupt_type_name'] = msg.get('被执行人失信行为具体情形')
        self.executive_person['performed_part'] = msg.get('已履行')
        self.executive_person['reg_date'] = msg.get('立案时间')
        self.executive_person['gist_id'] = msg.get('执行依据文号')
        self.executive_person['court_name'] = msg.get('执行法院')
        self.executive_person['sex'] = msg.get('性别')
        self.executive_person['case_code'] = msg.get('执行案号')
        self.executive_person['publish_date'] = msg.get('发布日期')
        self.executive_person['unperform_part'] = msg.get('未履行')
        self.executive_person['duty'] = msg.get('生效法律文书确定的义务')


    def bzx(self):
        print('{}:{}'.format(datetime.now(), self.path))
        d = pq(self.detail)
        l = pq(self.list)
        l_list = [each.text() for each in l(".td_cell").items()]
        l_list = l_list[1:4] if len(l_list) > 4 else ['', '', '']
        key_msg = [each.text() for n, each in enumerate(d(".td_cell").items()) if n % 2 == 0]
        value_msg = [each.text() for n, each in enumerate(d(".td_cell").items()) if n % 2 != 0]
        msg = dict(zip(key_msg, value_msg))
        msg = msg if msg else {'被执行人姓名/名称': l_list[0], '案号': l_list[1], '证件号码': l_list[2]}
        self.executive_announcement['name'] = msg.get('被执行人姓名/名称')
        self.executive_announcement['itype'] = msg.get('被执行人类型')
        self.executive_announcement['card_num'] = msg.get('证件号码') if msg.get('证件号码') else msg.get('组织机构代码')
        self.executive_announcement['business_entity'] = msg.get('法定代表人姓名')
        self.executive_announcement['sex'] = msg.get('被执行人性别')
        self.executive_announcement['age'] = msg.get('被执行人年龄')
        self.executive_announcement['execute_money'] = msg.get('申请执行标的金额')
        self.executive_announcement['reg_date'] = msg.get('立案日期')
        self.executive_announcement['court_name'] = msg.get('经办机构（做出执行依据单位）') if msg.get('经办机构（做出执行依据单位）') else msg.get('执行法院')
        self.executive_announcement['case_code'] = msg.get('案号')

