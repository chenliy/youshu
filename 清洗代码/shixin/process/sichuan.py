from IKEA.shixin.process.base_process import Base
import json
from lxml import etree
from datetime import datetime

class SiChuan(Base):
    def __init__(self,**kwargs):
        super(SiChuan,self).__init__(**kwargs)
        self.html = etree.HTML(self.list)
        self.results = self.html.xpath('//td')
        self.name = self.results[1].xpath('.//text()')[0] if self.results[1].xpath('.//text()') else ''
        self.card_num = self.results[3].xpath('.//text()')[0] if self.results[3].xpath('.//text()') else ''
        self.case_code = self.results[5].xpath('.//text()')[0] if self.results[5].xpath('.//text()') else ''
        self.duty = self.results[6].xpath('.//text()')[0] if self.results[6].xpath('.//text()') else ''
        self.court_name = self.results[7].xpath('.//text()')[0] if self.results[7].xpath('.//text()') else ''
        self.reg_date = self.results[8].xpath('.//text()')[0] if self.results[8].xpath('.//text()') else None

        pass

    def sxbzx(self):
        print('{}:{}'.format(datetime.now(), self.path))
        self.executive_person["source"] = self.path
        self.executive_person["area_name"] = '四川'
        self.executive_person["name"] = self.name
        self.executive_person["card_num"] = self.card_num
        self.executive_person["case_code"] = self.case_code
        self.executive_person["duty"] = self.duty
        self.executive_person["court_name"] = self.court_name
        self.executive_person["reg_date"] = self.reg_date
        self.executive_person['operator'] = 'wangfeng'
        # print(self.executive_person)
        

    def xzcj(self):
        print('{}:{}'.format(datetime.now(), self.path))
        # self.exposure_desk["exposure_type"] = self.exposure_type
        self.exposure_desk["source"] = self.path
        self.exposure_desk["name"] = self.name
        self.exposure_desk["card_num"] = self.card_num
        self.exposure_desk["case_code"] = self.case_code
        self.exposure_desk["duty"] = self.duty
        self.exposure_desk["court_name"] = self.court_name
        self.exposure_desk["reg_date"] = self.reg_date
        self.exposure_desk['operator'] = 'wangfeng'

        self.executive_announcement['operator'] = 'wangfeng'
        super().split_ex()
        

    def xzgxf(self):
        return self.xzcj()

    def xztzb(self):
        return self.xzcj()


if __name__ == '__main__':
    s = '''
        <tr height="30">
        <td align="center" class="bg1">10</td>
        <td align="center" class="bg1">马超</td>
        <td align="center" class="bg1">中华人民共和国居民身份证</td>
        <td align="center" class="bg1">510822197811243916</td>
        <td align="center" class="bg1">失信被执行人</td>
        <td align="center" class="bg1">(2016)川0822执65号</td>
        <td align="center" class="bg1">被执行人马超支付申请执行人刘玉发人民币1317259.00元。</td>
        <td align="center" class="bg1">青川</td>
        <td align="center" class="bg1">2016-01-25</td>
        </tr>
    '''
    sc = SiChuan(path='失信被执行人', list=s, detail=None)
    print(sc.sxbzx())


