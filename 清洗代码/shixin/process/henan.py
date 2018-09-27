import os
import sys
sys.path.append(os.path.abspath(__file__ + "/../../../../"))
from IKEA.shixin.process.base_process import Base
from IKEA.mysql.mysqlbase import MysqlBase
from IKEA.shixin.config import connecter
from pyquery import PyQuery as pq
from datetime import datetime

class HeNan(Base):

    def wjzxssaj(self):
        print('{}:{}'.format(datetime.now(), self.path))
        d = pq(self.detail)
        l = pq(self.list)
        name = l(".name").text()
        case_code = l(".num").text()
        p = [each for each in l(".zx-right").items()]
        (itype, card_num) = (p[0].text(), p[1].text()) if len(p) == 2 else ('', '')
        card_num = None if card_num == 'null' or card_num == '' else card_num
        itype = None if itype == 'null' or itype == '' else itype
        key_msg = [each.text() for n, each in enumerate(d("td").items()) if n % 2 == 0]
        value_msg = [each.text() for n, each in enumerate(d("td").items()) if n % 2 != 0]
        msg = dict(zip(key_msg, value_msg))

        msg = msg if msg else {'被执行人姓名/名称': name, '案号': case_code, '证件号码': card_num, '被执行人类型': itype}
        self.exposure_desk['identity'] = msg.get('诉讼地位')
        self.exposure_desk['name'] = msg.get('被执行人姓名/名称')
        self.exposure_desk['itype'] = msg.get('被执行人类型')
        self.exposure_desk['card_num'] = msg.get('证件号码') if msg.get('证件号码') else msg.get('组织机构代码')
        self.exposure_desk['case_code'] = msg.get('案号')
        self.exposure_desk['reg_date'] = msg.get('立案日期')
        self.exposure_desk['court_name'] = msg.get('执行法院')
        self.exposure_desk['reason'] = msg.get('执行案由')
        self.exposure_desk['case_status'] = msg.get('案件状态')
        self.exposure_desk['execute_money'] = msg.get('申请执行标的金额')
        self.exposure_desk['gist_id'] = msg.get('执行依据文书编号')
        self.exposure_desk['gist_unit'] = msg.get('经办机构（做出执行依据单位）')
        self.exposure_desk['release_date'] = msg.get('发布日期')
        self.exposure_desk['age'] = msg.get('被执行人年龄')
        self.exposure_desk['sex'] = msg.get('被执行人性别') if msg.get('被执行人性别') else msg.get('法定代表人性别')
        self.exposure_desk['business_entity'] = msg.get('法定代表人姓名')
        self.exposure_desk['address'] = msg.get('被执行人国家或地区')
        super().split_ex()

    def xzgxf(self):
        return self.wjzxssaj()

    def xzcj(self):
        return self.wjzxssaj()

    def xztzb(self):
        return self.wjzxssaj()

    def wszc(self):
        return self.wjzxssaj()

    def bgt(self):
        return self.wjzxssaj()



