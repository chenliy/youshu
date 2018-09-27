from IKEA.libs.date import update_time

class Base:
    """process base class
    process change path to different method, and if baoguangtai return beizhixing
    """
    def __init__(self, path, list, detail):
        self.path = path
        self.list = list
        self.detail = detail
        self.executive_person = {'update_time': update_time(), 'source': self.path, 'operator': 'leifeng'}
        self.executive_announcement = {'update_time': update_time(), 'source': self.path, 'operator': 'leifeng'}
        self.exposure_desk = {'update_time': update_time(), 'source': self.path, 'operator': 'leifeng'}

    def split_ex(self):
        """split baoguangtai to zhixingren and baoguangtai
        Args
            kwargs: baoguangtai dict
        Returns
            (beizhixing, baoguangtai):tuple beizhixing dict & baoguangtai dict
        """
        self.executive_announcement["notice_id"] = self.exposure_desk.get('notice_id')
        self.executive_announcement["name"] = self.exposure_desk.get('name')
        self.executive_announcement["name_id"] = self.exposure_desk.get('name_id')
        self.executive_announcement["itype"] = self.exposure_desk.get('itype')
        self.executive_announcement["card_num"] = self.exposure_desk.get('card_num')
        self.executive_announcement["business_entity"] = self.exposure_desk.get('business_entity')
        self.executive_announcement["sex"] = self.exposure_desk.get('sex')
        self.executive_announcement["age"] = self.exposure_desk.get('age')
        self.executive_announcement["address"] = self.exposure_desk.get('address')
        self.executive_announcement["execute_money"] = self.exposure_desk.get('execute_money')
        self.executive_announcement["unexecute_money"] = self.exposure_desk.get('unexecute_money')
        self.executive_announcement["case_code"] = self.exposure_desk.get('case_code')
        self.executive_announcement["reg_date"] = self.exposure_desk.get('reg_date')
        self.executive_announcement["court_name"] = self.exposure_desk.get('court_name')
        self.executive_announcement["source"] = self.exposure_desk.get('source')
        self.executive_announcement["case_id"] = self.exposure_desk.get('case_id')
        self.executive_announcement["date_created"] = self.exposure_desk.get('date_created')

    def baoguangtai(self):
        """baoguangtai porcess
        Return
            function: subclass overwrite function, process baoguangtai dict
        """
        if '未结执行实施案件' in self.path:
            self.exposure_desk['exposure_type'] = '未结执行实施案件'
            return self.wjzxssaj()
        elif '限制出境' in self.path:
            self.exposure_desk['exposure_type'] = '限制出境'
            return self.xzcj()
        elif '限制高消费' in self.path:
            self.exposure_desk['exposure_type'] = '限制高消费'
            return self.xzgxf()
        elif '限制招投标' in self.path:
            self.exposure_desk['exposure_type'] = '限制招投标'
            return self.xztzb()
        elif '网上追查' in self.path:
            self.exposure_desk['exposure_type'] = '网上追查'
            return self.wszc()
        elif '曝光台' in self.path:
            self.exposure_desk['exposure_type'] = '曝光台'
            return self.bgt()


    def shixin(self):
        if '失信' in self.path:
            return self.sxbzx()

    def beizhixing(self):
        if '失信' not in self.path and '被执行' in self.path:
            return self.bzx()

