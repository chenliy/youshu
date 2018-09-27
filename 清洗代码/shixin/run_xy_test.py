import os
import sys
sys.path.append(os.path.abspath(__file__ + "/../../../"))
from IKEA.mysql.mysqlbase import MysqlBase
from IKEA.shixin.config import connecter as connecter
from IKEA.shixin.process.zhejiang import ZheJiang
from IKEA.shixin.process.gansu import GanSu
from IKEA.shixin.process.guangxi import GuangXi
from IKEA.shixin.process.guizhou import GuiZhou
from IKEA.shixin.process.hebei import Hebei
from IKEA.shixin.process.henan import HeNan
from IKEA.shixin.process.xinjiang import Xinjiang
from IKEA.shixin.process.anhui import AnHui
from IKEA.shixin.process.beijing import BeiJing
from IKEA.shixin.process.chongqing import ChongQing
from IKEA.shixin.process.liaoning import LiaoNing
from IKEA.shixin.process.qinghai import QingHai
from IKEA.shixin.process.sichuan import SiChuan
from IKEA.shixin.process.yunnan import YunNan
from IKEA.es.postelastic import ines
from IKEA.shixin.libs.id import get_md5
from IKEA.shixin.libs.itype import itype
from IKEA.shixin.config import exposure_desk_path
from IKEA.shixin.config import executive_announcement_gaoyuan_path
from IKEA.shixin.config import executive_announcement_total_path
from IKEA.shixin.config import executive_person_gaoyuan_path
from IKEA.shixin.config import executive_person_total_path
from IKEA.shixin.config import host_url as host_url
from datetime import datetime
import json
import re


def run(items):
    _exposure_desk_path = host_url + '/' + exposure_desk_path
    _executive_announcement_total_path = host_url + '/' + executive_announcement_total_path
    _executive_announcement_gaoyuan_path = host_url + '/' + executive_announcement_gaoyuan_path
    _executive_person_total_path = host_url + '/' + executive_person_total_path
    _executive_person_gaoyuan_path = host_url + '/' + executive_person_gaoyuan_path


    if '安徽' in items['data_path']:
        ah = AnHui(path=items['data_path'], list=items['list_response'], detail=items['detail_response'])
        ah.shixin()
        ah.baoguangtai()
        if ah.executive_announcement.get('case_code') and ah.executive_announcement.get('name'):
            _executive_announcement_id = (bytes(ah.executive_announcement.get('name') + ah.executive_announcement.get('case_code'), encoding='utf-8'))
            executive_announcement_id = get_md5(_executive_announcement_id)
            ah.executive_announcement['id'] = executive_announcement_id
            ines(id=executive_announcement_id, path=_executive_announcement_gaoyuan_path, data=itype(ah.executive_announcement))
            ines(id=executive_announcement_id, path=_executive_announcement_total_path, data=itype(ah.executive_announcement))
            exposure_desk_id = executive_announcement_id + get_md5(bytes(ah.exposure_desk.get('exposure_type'), encoding='utf-8'))
            ah.exposure_desk['id'] = exposure_desk_id
            # ines(id=exposure_desk_id, path=_exposure_desk_path, data=itype(ah.exposure_desk))
        if ah.executive_person.get('case_code') and ah.executive_person.get('name'):
            executive_person_id = get_md5(bytes(ah.executive_person.get('name')+ah.executive_person.get('case_code'), encoding='utf-8'))
            ah.executive_person['id'] = executive_person_id
            # print(ah.executive_person)
            ines(id=executive_person_id, path=_executive_person_total_path, data=ah.executive_person)
            ines(id=executive_person_id, path=_executive_person_gaoyuan_path, data=ah.executive_person)

    elif '北京' in items['data_path']:
        bj = BeiJing(path=items['data_path'], list=items['list_response'], detail=items['detail_response'])
        bj.shixin()
        bj.baoguangtai()
        # print(bj.executive_announcement)
        if bj.executive_announcement.get('case_code') and bj.executive_announcement.get('name'):
            _executive_announcement_id = (bytes(bj.executive_announcement.get('name') + bj.executive_announcement.get('case_code'), encoding='utf-8'))
            executive_announcement_id = get_md5(_executive_announcement_id)
            bj.executive_announcement['id'] = executive_announcement_id
            ines(id=executive_announcement_id, path=_executive_announcement_gaoyuan_path, data=itype(bj.executive_announcement))
            ines(id=executive_announcement_id, path=_executive_announcement_total_path, data=itype(bj.executive_announcement))
            exposure_desk_id = executive_announcement_id + get_md5(bytes(bj.exposure_desk.get('exposure_type'), encoding='utf-8'))
            bj.exposure_desk['id'] = exposure_desk_id
            # ines(id=exposure_desk_id, path=_exposure_desk_path, data=itype(bj.exposure_desk))
        if bj.executive_person.get('case_code') and bj.executive_person.get('name'):
            executive_person_id = get_md5(bytes(bj.executive_person.get('name')+bj.executive_person.get('case_code'), encoding='utf-8'))
            bj.executive_person['id'] = executive_person_id
            # print(bj.executive_person)
            ines(id=executive_person_id, path=_executive_person_total_path, data=bj.executive_person)
            ines(id=executive_person_id, path=_executive_person_gaoyuan_path, data=bj.executive_person)

    elif '重庆' in items['data_path']:
        cq = ChongQing(path=items['data_path'], list=items['list_response'], detail=items['detail_response'])
        cq.shixin()
        cq.baoguangtai()
        if cq.executive_announcement.get('case_code') and cq.executive_announcement.get('name'):
            _executive_announcement_id = (bytes(cq.executive_announcement.get('name') + cq.executive_announcement.get('case_code'), encoding='utf-8'))
            executive_announcement_id = get_md5(_executive_announcement_id)
            cq.executive_announcement['id'] = executive_announcement_id
            ines(id=executive_announcement_id, path=_executive_announcement_gaoyuan_path, data=itype(cq.executive_announcement))
            ines(id=executive_announcement_id, path=_executive_announcement_total_path,
                 data=itype(cq.executive_announcement))

            exposure_desk_id = executive_announcement_id + get_md5(bytes(cq.exposure_desk.get('exposure_type'), encoding='utf-8'))
            cq.exposure_desk['id'] = exposure_desk_id
            # ines(id=exposure_desk_id, path=_exposure_desk_path, data=itype(cq.exposure_desk))
        if cq.executive_person.get('case_code') and cq.executive_person.get('name'):
            executive_person_id = get_md5(bytes(cq.executive_person.get('name')+cq.executive_person.get('case_code'), encoding='utf-8'))
            cq.executive_person['id'] = executive_person_id
            ines(id=executive_person_id, path=_executive_person_total_path, data=cq.executive_person)
            ines(id=executive_person_id, path=_executive_person_gaoyuan_path, data=cq.executive_person)

    elif '辽宁' in items['data_path']:
        ln = LiaoNing(path=items['data_path'], list=items['list_response'], detail=items['detail_response'])
        ln.shixin()
        ln.baoguangtai()
        if ln.executive_announcement.get('case_code') and ln.executive_announcement.get('name'):
            _executive_announcement_id = (bytes(ln.executive_announcement.get('name') + ln.executive_announcement.get('case_code'), encoding='utf-8'))
            executive_announcement_id = get_md5(_executive_announcement_id)
            ln.executive_announcement['id'] = executive_announcement_id
            ines(id=executive_announcement_id, path=_executive_announcement_total_path, data=itype(ln.executive_announcement))
            ines(id=executive_announcement_id, path=_executive_announcement_gaoyuan_path, data=itype(ln.executive_announcement))
            exposure_desk_id = executive_announcement_id + get_md5(bytes(ln.exposure_desk.get('exposure_type'), encoding='utf-8'))
            ln.exposure_desk['id'] = exposure_desk_id
            # ines(id=exposure_desk_id, path=_exposure_desk_path, data=itype(ln.exposure_desk))
        if ln.executive_person.get('case_code') and ln.executive_person.get('name'):
            executive_person_id = get_md5(bytes(ln.executive_person.get('name')+ln.executive_person.get('case_code'), encoding='utf-8'))
            ln.executive_person['id'] = executive_person_id
            ines(id=executive_person_id, path=_executive_person_total_path, data=ln.executive_person)
            ines(id=executive_person_id, path=_executive_person_gaoyuan_path, data=ln.executive_person)

    elif '青海' in items['data_path']:
        qh = QingHai(path=items['data_path'], list=items['list_response'], detail=items['detail_response'])
        qh.shixin()
        qh.baoguangtai()
        if qh.executive_announcement.get('case_code') and qh.executive_announcement.get('name'):
            _executive_announcement_id = (bytes(qh.executive_announcement.get('name') + qh.executive_announcement.get('case_code'), encoding='utf-8'))
            executive_announcement_id = get_md5(_executive_announcement_id)
            qh.executive_announcement['id'] = executive_announcement_id
            ines(id=executive_announcement_id, path=_executive_announcement_total_path, data=itype(qh.executive_announcement))
            ines(id=executive_announcement_id, path=_executive_announcement_path, data=itype(qh.executive_announcement))

            exposure_desk_id = executive_announcement_id + get_md5(bytes(qh.exposure_desk.get('exposure_type'), encoding='utf-8'))
            qh.exposure_desk['id'] = exposure_desk_id
            # ines(id=exposure_desk_id, path=_exposure_desk_path, data=itype(qh.exposure_desk))
        if qh.executive_person.get('case_code') and qh.executive_person.get('name'):
            executive_person_id = get_md5(bytes(qh.executive_person.get('name')+qh.executive_person.get('case_code'), encoding='utf-8'))
            qh.executive_person['id'] = executive_person_id
            ines(id=executive_person_id, path=_executive_person_gaoyuan_path, data=qh.executive_person)
            ines(id=executive_person_id, path=_executive_person_total_path, data=qh.executive_person)

    elif '四川' in items['data_path']:
        sc = SiChuan(path=items['data_path'], list=items['list_response'], detail=items['detail_response'])
        sc.shixin()
        sc.baoguangtai()
        if sc.executive_announcement.get('case_code') and sc.executive_announcement.get('name'):
            _executive_announcement_id = (bytes(sc.executive_announcement.get('name') + sc.executive_announcement.get('case_code'), encoding='utf-8'))
            executive_announcement_id = get_md5(_executive_announcement_id)
            sc.executive_announcement['id'] = executive_announcement_id
            ines(id=executive_announcement_id, path=_executive_announcement_gaoyuan_path, data=itype(sc.executive_announcement))
            ines(id=executive_announcement_id, path=_executive_announcement_total_path, data=itype(sc.executive_announcement))
            exposure_desk_id = executive_announcement_id + get_md5(bytes(sc.exposure_desk.get('exposure_type'), encoding='utf-8'))
            sc.exposure_desk['id'] = exposure_desk_id
            # ines(id=exposure_desk_id, path=_exposure_desk_path, data=itype(sc.exposure_desk))
        if sc.executive_person.get('case_code') and sc.executive_person.get('name'):
            executive_person_id = get_md5(bytes(sc.executive_person.get('name')+sc.executive_person.get('case_code'), encoding='utf-8'))
            sc.executive_person['id'] = executive_person_id
            ines(id=executive_person_id, path=_executive_person_total_path, data=sc.executive_person)
            ines(id=executive_person_id, path=_executive_person_gaoyuan_path, data=sc.executive_person)
    
if __name__ == '__main__':
    # 0表示未结构化   1成功结构化  2结构化出错  3缺少list或者detail 4表示es插入问题
    # logerror      100        200        300  301缺少detail         400
    data_paths = [
        '安徽高级人民法院-执行信息-未结执行实施案件',
        '安徽高级人民法院-执行信息-失信被执行人',
        '北京法院审判信息网-执行信息-限制高消费被执行人',
        '北京法院审判信息网-执行信息-失信被执行人',
        '北京法院审判信息网-执行信息-限制出境被执行人',
        '北京法院审判信息网-执行信息-限制招投标被执行人',
        '重庆法院公众服务网-执行信息-失信被执行人',
        '重庆法院公众服务网-执行信息-限制出境',
        '重庆法院公众服务网-执行信息-限制高消费被执行人',
        '辽宁高院审批信息网-执行信息-失信被执行人',
        '辽宁高院审批信息网-执行信息-未结执行实施案件',
        '辽宁高院审批信息网-执行信息-限制出境',
        '辽宁高院审批信息网-执行信息-限制招投标',
        '辽宁高院审批信息网-执行信息-限制高消费',
        '青海法院审批信息网-执行信息-失信被执行人',
        '青海法院审批信息网-执行信息-未结执行实施案件',
        '四川法院司法公开网-执行信息-限制招投标',
        '四川法院司法公开网-执行信息-限制高消费',
        '四川法院司法公开网-执行信息-失信被执行人',
        '四川法院司法公开网-执行信息-限制出境',
    ]
    data_paths = [
        '甘肃法院诉讼无忧-执行信息-未结执行实施案件',
        '甘肃法院诉讼无忧-执行信息-限制高消费',
        '广西法院阳光司法网-执行信息-失信被执行人',
        '广西法院阳光司法网-执行信息-未结执行实施案件',
        '广西法院阳光司法网-执行信息-限制出境',
        '广西法院阳光司法网-执行信息-限制高消费',
        '贵州法院诉讼服务网-执行信息-失信被执行人',
        '贵州法院诉讼服务网-执行信息-未结执行实施案件',
        '河北省高级人民法院网-执行信息-失信人',
        '河北省高级人民法院网-执行信息-未结执行实施案件',
        '河北省高级人民法院网-执行信息-限制出境',
        '河北省高级人民法院网-执行信息-限制招投标',
        '河北省高级人民法院网-执行信息-限制高消费人',
        '河南法院诉讼服务网-执行信息-未结执行实施案件',
        '新疆法院诉讼服务网-执行信息-失信被执行人',
        '新疆法院诉讼服务网-执行信息-被执行人',
        '上海市高级人民法院网-执行信息-曝光台',
        '上海市高级人民法院网-执行信息-网上追查',
        '上海市高级人民法院网-执行信息-限制出境',
        '上海市高级人民法院网-执行信息-限制高消费',
        '浙江法院公开网 - 执行信息 - 曝光台(个人)',
        '浙江法院公开网 - 执行信息 - 限制出境',
        '浙江法院公开网 - 执行信息 - 限制招投标',
        '浙江法院公开网 - 执行信息 - 限制高消费'
    ]
    mb = MysqlBase(connecter)
    a = -1
    while 1:
        a = a + 1
        for data_path in data_paths:
            if '四川' in data_path:
                table = 'zhixing'
                for items in mb._execute(
                        "select * from zhixing where data_path='{}' order by id limit {},10000;".format(
                                data_path, a*10000)):
                    try:
                        run(items)
                        mb._update("UPDATE {} SET is_process = {} WHERE  id= '{}'".format(table, items['id']), 100)
                    except:
                        mb._update("UPDATE {} SET is_process = {} WHERE  id= '{}'".format(table, items['id'], 200))
                        pass
            else:
                for items in mb._execute("select * from zhixing_no_detail where  data_path='{}' order by id  limit {},10000;".format(data_path,a*10000)):
                    table = 'zhixing_no_detail'
                    try:
                        run(items)
                        mb._update("UPDATE {} SET is_process = {} WHERE  id= '{}'".format(table, items['id']), 100)
                    except:
                        mb._update("UPDATE {} SET is_process = {} WHERE  id= '{}'".format(table, items['id'], 200))
                        pass
