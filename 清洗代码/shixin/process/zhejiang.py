from IKEA.shixin.process.base_process import Base
import json
from datetime import datetime

class ZheJiang(Base):
    def wjzxssaj(self):
        print('{}:{}'.format(datetime.now(), self.path))
        msg = self.list
        self.exposure_desk["address"] = msg.get('Address')
        self.exposure_desk["unexecute_money"] = msg.get('WZXJE')
        self.exposure_desk["case_code"] = msg.get('AH')
        self.exposure_desk["card_num"] = msg.get('CredentialsNumber')
        self.exposure_desk["reg_date"] = msg.get('LARQ')
        self.exposure_desk["name"] = msg.get('ReallyName')
        self.exposure_desk["reason"] = msg.get('ZXAY')
        self.exposure_desk["court_name"] = msg.get('ZXFY')
        self.exposure_desk["execute_money"] = msg.get('ZXJE')
        self.exposure_desk["release_date"] = msg.get('BGRQ')
        super().split_ex()

    def xzcj(self):
        return self.wjzxssaj()

    def xzgxf(self):
        return self.wjzxssaj()

    def xztzb(self):
        return self.wjzxssaj()

    def wszc(self):
        return self.wjzxssaj()

    def bgt(self):
        return self.wjzxssaj()

