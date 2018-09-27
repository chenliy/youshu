import os
import sys
sys.path.append(os.path.abspath(__file__ + "/../../../"))
from IKEA.mysql.mysqlbase import MysqlBase
from IKEA.shixin.process.zhejiang import ZheJiang
from IKEA.shixin.process.gansu import GanSu
from IKEA.shixin.process.guangxi import GuangXi
from IKEA.shixin.process.guizhou import GuiZhou
from IKEA.shixin.process.hebei import Hebei
from IKEA.shixin.process.henan import HeNan
from IKEA.shixin.process.xinjiang import Xinjiang
from IKEA.shixin.process.yunnan import YunNan
from IKEA.shixin.process.shanghai import ShangHai
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
from IKEA.shixin.config import p_connecter as connecter
from datetime import datetime
import json
import re


def run(items):
    _exposure_desk_path = host_url + '/' + exposure_desk_path
    _executive_announcement_total_path = host_url + '/' + executive_announcement_total_path
    _executive_announcement_gaoyuan_path = host_url + '/' + executive_announcement_gaoyuan_path
    _executive_person_total_path = host_url + '/' + executive_person_total_path
    _executive_person_gaoyuan_path = host_url + '/' + executive_person_gaoyuan_path



    if '浙江' in items['data_path']:
        l = eval(re.sub('/', '', items['list_response']))
        zj = ZheJiang(path=items['data_path'], list=l, detail=items['detail_response'])
        zj.baoguangtai()
        exposure_desk = zj.exposure_desk
        executive_announcement = zj.executive_announcement
        if zj.executive_announcement.get('case_code') and zj.executive_announcement.get('name'):
            exposure_desk_id = get_md5(bytes(exposure_desk.get('name') + exposure_desk.get('case_code'), encoding='utf-8')) + get_md5(bytes(exposure_desk.get('exposure_type'), encoding='utf-8'))
            exposure_desk['id'] = exposure_desk_id
            executive_announcement_id = get_md5(bytes(executive_announcement.get('name') + executive_announcement.get('case_code'), encoding='utf-8'))
            executive_announcement['id'] = executive_announcement_id
            ines(id=exposure_desk_id, path=_exposure_desk_path, data=itype(exposure_desk))
            ines(id=executive_announcement_id, path=_executive_announcement_total_path, data=itype(executive_announcement))
            ines(id=executive_announcement_id, path=_executive_announcement_gaoyuan_path,
                 data=itype(executive_announcement))


    elif '甘肃' in items['data_path']:
        gs = GanSu(path=items['data_path'], list=items['list_response'], detail=items['detail_response'])
        gs.baoguangtai()
        if gs.executive_announcement.get('case_code') and gs.executive_announcement.get('name'):
            _executive_announcement_id = (bytes(gs.executive_announcement.get('name') + gs.executive_announcement.get('case_code'), encoding='utf-8'))
            executive_announcement_id = get_md5(_executive_announcement_id)
            gs.executive_announcement['id'] = executive_announcement_id
            ines(id=executive_announcement_id, path=_executive_announcement_gaoyuan_path, data=itype(gs.executive_announcement))
            ines(id=executive_announcement_id, path=_executive_announcement_total_path, data=itype(gs.executive_announcement))
            exposure_desk_id = get_md5(bytes(gs.exposure_desk.get('name') + gs.exposure_desk.get('case_code'), encoding='utf-8')) + get_md5(bytes(gs.exposure_desk.get('exposure_type'), encoding='utf-8'))
            gs.exposure_desk['id'] = exposure_desk_id
            ines(id=exposure_desk_id, path=_exposure_desk_path, data=itype(gs.exposure_desk))

    elif '广西' in items['data_path']:
        gx = GuangXi(path=items['data_path'], list=items['list_response'], detail=items['detail_response'])
        gx.shixin()
        gx.baoguangtai()
        if gx.executive_announcement.get('case_code') and gx.executive_announcement.get('name'):
            executive_announcement_id = get_md5(bytes(gx.executive_announcement['case_code'] + gx.executive_announcement['name'], encoding='utf-8'))
            exposure_desk_id = get_md5(bytes(gx.exposure_desk['exposure_type'], encoding='utf-8')) + executive_announcement_id
            gx.exposure_desk['id'] = exposure_desk_id
            gx.executive_announcement['id'] = executive_announcement_id
            ines(id=executive_announcement_id, path=_executive_announcement_gaoyuan_path, data=itype(gx.executive_announcement))
            ines(id=executive_announcement_id, path=_executive_announcement_total_path, data=itype(gx.executive_announcement))
            ines(id=exposure_desk_id, path=_exposure_desk_path, data=itype(gx.exposure_desk))
        if gx.executive_person.get('case_code') and gx.executive_person.get('name'):
            executive_person_id = get_md5(bytes(gx.executive_person['case_code'] + gx.executive_person['name'], encoding='utf-8'))
            gx.executive_person['id'] = executive_person_id
            ines(id=executive_person_id, path=_executive_person_total_path, data=gx.executive_person)
            ines(id=executive_person_id, path=_executive_person_gaoyuan_path, data=gx.executive_person)

    elif '贵州' in items['data_path']:
        gz = GuiZhou(path=items['data_path'], list=items['list_response'], detail=items['detail_response'])
        gz.shixin()
        gz.baoguangtai()
        if gz.executive_announcement.get('case_code') and gz.executive_announcement.get('name'):
            executive_announcement_id = get_md5(bytes(gz.executive_announcement['case_code'] + gz.executive_announcement['name'], encoding='utf-8'))
            exposure_desk_id = get_md5(bytes(gz.exposure_desk['exposure_type'], encoding='utf-8')) + executive_announcement_id
            gz.exposure_desk['id'] = exposure_desk_id
            gz.executive_announcement['id'] = executive_announcement_id
            ines(id=executive_announcement_id, path=_executive_announcement_gaoyuan_path, data=itype(gz.executive_announcement))
            ines(id=executive_announcement_id, path=_executive_announcement_total_path, data=itype(gz.executive_announcement))
            ines(id=exposure_desk_id, path=_exposure_desk_path, data=itype(gz.exposure_desk))
        if gz.executive_person.get('case_code') and gz.executive_person.get('name'):
            executive_person_id = get_md5(bytes(gz.executive_person['name'] + gz.executive_person['case_code'], encoding='utf-8'))
            gz.executive_person['id'] = executive_person_id
            ines(id=executive_person_id, path=_executive_person_total_path, data=gz.executive_person)
            ines(id=executive_person_id, path=_executive_person_gaoyuan_path, data=gz.executive_person)

    elif '河北' in items['data_path']:
        hb = Hebei(path=items['data_path'], list=items['list_response'], detail=items['detail_response'])
        hb.shixin()
        hb.baoguangtai()
        if hb.executive_announcement.get('case_code') and hb.executive_announcement.get('name'):
            executive_announcement_id = get_md5(
                bytes(hb.executive_announcement['case_code'] + hb.executive_announcement['name'], encoding='utf-8'))
            exposure_desk_id = get_md5(
                bytes(hb.exposure_desk['exposure_type'], encoding='utf-8')) + executive_announcement_id
            hb.executive_announcement['id'] = executive_announcement_id
            hb.exposure_desk['id'] = exposure_desk_id
            ines(id=executive_announcement_id, path=_executive_announcement_gaoyuan_path, data=itype(hb.executive_announcement))
            ines(id=executive_announcement_id, path=_executive_announcement_total_path, data=itype(hb.executive_announcement))
            ines(id=exposure_desk_id, path=_exposure_desk_path, data=itype(hb.exposure_desk))
        if hb.executive_person.get('case_code') and hb.executive_person.get('name'):
            executive_person_id = get_md5(
                bytes(hb.executive_person['name'] + hb.executive_person['case_code'], encoding='utf-8'))
            hb.executive_person['id'] = executive_person_id
            ines(id=executive_person_id, path=_executive_person_gaoyuan_path, data=hb.executive_person)
            ines(id=executive_person_id, path=_executive_person_total_path, data=hb.executive_person)


    elif '河南' in items['data_path']:
        hn = HeNan(path=items['data_path'], list=items['list_response'], detail=items['detail_response'])
        hn.baoguangtai()
        if hn.executive_announcement.get('case_code') and hn.executive_announcement.get('name'):
            _executive_announcement_id = (bytes(hn.executive_announcement.get('name') + hn.executive_announcement.get('case_code'), encoding='utf-8'))
            executive_announcement_id = get_md5(_executive_announcement_id)
            hn.executive_announcement['id'] = executive_announcement_id
            ines(id=executive_announcement_id, path=_executive_announcement_gaoyuan_path, data=itype(hn.executive_announcement))
            ines(id=executive_announcement_id, path=_executive_announcement_total_path, data=itype(hn.executive_announcement))
            exposure_desk_id = executive_announcement_id + get_md5(bytes(hn.exposure_desk.get('exposure_type'), encoding='utf-8'))
            hn.exposure_desk['id'] = exposure_desk_id
            ines(id=exposure_desk_id, path=_exposure_desk_path, data=itype(hn.exposure_desk))

    elif '新疆' in items['data_path']:
        xj = Xinjiang(path=items['data_path'], list=items['list_response'], detail=items['detail_response'])
        xj.shixin()
        xj.beizhixing()
        if xj.executive_announcement.get('case_code') and xj.executive_announcement.get('name'):
            _executive_announcement_id = (bytes(xj.executive_announcement.get('name') + xj.executive_announcement.get('case_code'), encoding='utf-8'))
            executive_announcement_id = get_md5(_executive_announcement_id)
            xj.executive_announcement['id'] = executive_announcement_id
            ines(id=executive_announcement_id, path=_executive_announcement_total_path, data=itype(xj.executive_announcement))
            ines(id=executive_announcement_id, path=_executive_announcement_gaoyuan_path, data=itype(xj.executive_announcement))
        if xj.executive_person.get('case_code') and xj.executive_person.get('name'):
            executive_person_id = get_md5(bytes(xj.executive_person.get('case_code')+xj.executive_person.get('name'), encoding='utf-8'))
            xj.executive_person['id'] = executive_person_id
            ines(id=executive_person_id, path=_executive_person_total_path, data=xj.executive_person)
            ines(id=executive_person_id, path=_executive_person_gaoyuan_path, data=xj.executive_person)


    elif '上海' in items['data_path']:
        sh = ShangHai(path=items['data_path'], list=items['list_response'], detail=items['detail_response'])
        sh.baoguangtai()
        if sh.exposure_desk.get('case_code') and sh.exposure_desk.get('name'):
            _executive_announcement_id = (bytes(sh.executive_announcement.get('name') + sh.executive_announcement.get('case_code'), encoding='utf-8'))
            executive_announcement_id = get_md5(_executive_announcement_id)
            sh.executive_announcement['id'] = executive_announcement_id
            ines(id=executive_announcement_id, path=_executive_announcement_total_path, data=itype(sh.executive_announcement))
            ines(id=executive_announcement_id, path=_executive_announcement_gaoyuan_path, data=itype(sh.executive_announcement))
            exposure_desk_id = executive_announcement_id + get_md5(bytes(sh.exposure_desk.get('exposure_type'), encoding='utf-8'))
            sh.exposure_desk['id'] = exposure_desk_id
            ines(id=exposure_desk_id, path=_exposure_desk_path, data=itype(sh.exposure_desk))

    elif '安徽' in items['data_path']:
        ah = AnHui(path=items['data_path'], list=items['list_response'], detail=items['detail_response'])
        ah.shixin()
        ah.baoguangtai()
        if ah.executive_announcement.get('case_code') and ah.executive_announcement.get('name'):
            _executive_announcement_id = (
            bytes(ah.executive_announcement.get('name') + ah.executive_announcement.get('case_code'), encoding='utf-8'))
            executive_announcement_id = get_md5(_executive_announcement_id)
            ah.executive_announcement['id'] = executive_announcement_id
            ines(id=executive_announcement_id, path=_executive_announcement_gaoyuan_path,
                 data=itype(ah.executive_announcement))
            ines(id=executive_announcement_id, path=_executive_announcement_total_path,
                 data=itype(ah.executive_announcement))
            exposure_desk_id = executive_announcement_id + get_md5(
                bytes(ah.exposure_desk.get('exposure_type'), encoding='utf-8'))
            ah.exposure_desk['id'] = exposure_desk_id
            ines(id=exposure_desk_id, path=_exposure_desk_path, data=itype(ah.exposure_desk))
        if ah.executive_person.get('case_code') and ah.executive_person.get('name'):
            executive_person_id = get_md5(
                bytes(ah.executive_person.get('name') + ah.executive_person.get('case_code'), encoding='utf-8'))
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
            _executive_announcement_id = (
            bytes(bj.executive_announcement.get('name') + bj.executive_announcement.get('case_code'), encoding='utf-8'))
            executive_announcement_id = get_md5(_executive_announcement_id)
            bj.executive_announcement['id'] = executive_announcement_id
            ines(id=executive_announcement_id, path=_executive_announcement_gaoyuan_path,
                 data=itype(bj.executive_announcement))
            ines(id=executive_announcement_id, path=_executive_announcement_total_path,
                 data=itype(bj.executive_announcement))
            exposure_desk_id = executive_announcement_id + get_md5(
                bytes(bj.exposure_desk.get('exposure_type'), encoding='utf-8'))
            bj.exposure_desk['id'] = exposure_desk_id
            ines(id=exposure_desk_id, path=_exposure_desk_path, data=itype(bj.exposure_desk))
        if bj.executive_person.get('case_code') and bj.executive_person.get('name'):
            executive_person_id = get_md5(
                bytes(bj.executive_person.get('name') + bj.executive_person.get('case_code'), encoding='utf-8'))
            bj.executive_person['id'] = executive_person_id
            # print(bj.executive_person)
            ines(id=executive_person_id, path=_executive_person_total_path, data=bj.executive_person)
            ines(id=executive_person_id, path=_executive_person_gaoyuan_path, data=bj.executive_person)

    elif '重庆' in items['data_path']:
        cq = ChongQing(path=items['data_path'], list=items['list_response'], detail=items['detail_response'])
        cq.shixin()
        cq.baoguangtai()
        if cq.executive_announcement.get('case_code') and cq.executive_announcement.get('name'):
            _executive_announcement_id = (
            bytes(cq.executive_announcement.get('name') + cq.executive_announcement.get('case_code'), encoding='utf-8'))
            executive_announcement_id = get_md5(_executive_announcement_id)
            cq.executive_announcement['id'] = executive_announcement_id
            ines(id=executive_announcement_id, path=_executive_announcement_gaoyuan_path,
                 data=itype(cq.executive_announcement))
            ines(id=executive_announcement_id, path=_executive_announcement_total_path,
                 data=itype(cq.executive_announcement))

            exposure_desk_id = executive_announcement_id + get_md5(
                bytes(cq.exposure_desk.get('exposure_type'), encoding='utf-8'))
            cq.exposure_desk['id'] = exposure_desk_id
            ines(id=exposure_desk_id, path=_exposure_desk_path, data=itype(cq.exposure_desk))
        if cq.executive_person.get('case_code') and cq.executive_person.get('name'):
            executive_person_id = get_md5(
                bytes(cq.executive_person.get('name') + cq.executive_person.get('case_code'), encoding='utf-8'))
            cq.executive_person['id'] = executive_person_id
            ines(id=executive_person_id, path=_executive_person_total_path, data=cq.executive_person)
            ines(id=executive_person_id, path=_executive_person_gaoyuan_path, data=cq.executive_person)

    elif '辽宁' in items['data_path']:
        ln = LiaoNing(path=items['data_path'], list=items['list_response'], detail=items['detail_response'])
        ln.shixin()
        ln.baoguangtai()
        if ln.executive_announcement.get('case_code') and ln.executive_announcement.get('name'):
            _executive_announcement_id = (
            bytes(ln.executive_announcement.get('name') + ln.executive_announcement.get('case_code'), encoding='utf-8'))
            executive_announcement_id = get_md5(_executive_announcement_id)
            ln.executive_announcement['id'] = executive_announcement_id
            ines(id=executive_announcement_id, path=_executive_announcement_total_path,
                 data=itype(ln.executive_announcement))
            ines(id=executive_announcement_id, path=_executive_announcement_gaoyuan_path,
                 data=itype(ln.executive_announcement))
            exposure_desk_id = executive_announcement_id + get_md5(
                bytes(ln.exposure_desk.get('exposure_type'), encoding='utf-8'))
            ln.exposure_desk['id'] = exposure_desk_id
            ines(id=exposure_desk_id, path=_exposure_desk_path, data=itype(ln.exposure_desk))
        if ln.executive_person.get('case_code') and ln.executive_person.get('name'):
            executive_person_id = get_md5(
                bytes(ln.executive_person.get('name') + ln.executive_person.get('case_code'), encoding='utf-8'))
            ln.executive_person['id'] = executive_person_id
            ines(id=executive_person_id, path=_executive_person_total_path, data=ln.executive_person)
            ines(id=executive_person_id, path=_executive_person_gaoyuan_path, data=ln.executive_person)

    elif '青海' in items['data_path']:
        qh = QingHai(path=items['data_path'], list=items['list_response'], detail=items['detail_response'])
        qh.shixin()
        qh.baoguangtai()
        if qh.executive_announcement.get('case_code') and qh.executive_announcement.get('name'):
            _executive_announcement_id = (
            bytes(qh.executive_announcement.get('name') + qh.executive_announcement.get('case_code'), encoding='utf-8'))
            executive_announcement_id = get_md5(_executive_announcement_id)
            qh.executive_announcement['id'] = executive_announcement_id
            ines(id=executive_announcement_id, path=_executive_announcement_total_path,
                 data=itype(qh.executive_announcement))
            ines(id=executive_announcement_id, path=_executive_announcement_gaoyuan_path, data=itype(qh.executive_announcement))

            exposure_desk_id = executive_announcement_id + get_md5(
                bytes(qh.exposure_desk.get('exposure_type'), encoding='utf-8'))
            qh.exposure_desk['id'] = exposure_desk_id
            ines(id=exposure_desk_id, path=_exposure_desk_path, data=itype(qh.exposure_desk))
        if qh.executive_person.get('case_code') and qh.executive_person.get('name'):
            executive_person_id = get_md5(
                bytes(qh.executive_person.get('name') + qh.executive_person.get('case_code'), encoding='utf-8'))
            qh.executive_person['id'] = executive_person_id
            ines(id=executive_person_id, path=_executive_person_gaoyuan_path, data=qh.executive_person)
            ines(id=executive_person_id, path=_executive_person_total_path, data=qh.executive_person)

    elif '四川' in items['data_path']:
        sc = SiChuan(path=items['data_path'], list=items['list_response'], detail=items['detail_response'])
        sc.shixin()
        sc.baoguangtai()
        if sc.executive_announcement.get('case_code') and sc.executive_announcement.get('name'):
            _executive_announcement_id = (
            bytes(sc.executive_announcement.get('name') + sc.executive_announcement.get('case_code'), encoding='utf-8'))
            executive_announcement_id = get_md5(_executive_announcement_id)
            sc.executive_announcement['id'] = executive_announcement_id
            ines(id=executive_announcement_id, path=_executive_announcement_gaoyuan_path,
                 data=itype(sc.executive_announcement))
            ines(id=executive_announcement_id, path=_executive_announcement_total_path,
                 data=itype(sc.executive_announcement))
            exposure_desk_id = executive_announcement_id + get_md5(
                bytes(sc.exposure_desk.get('exposure_type'), encoding='utf-8'))
            sc.exposure_desk['id'] = exposure_desk_id
            ines(id=exposure_desk_id, path=_exposure_desk_path, data=itype(sc.exposure_desk))
        if sc.executive_person.get('case_code') and sc.executive_person.get('name'):
            executive_person_id = get_md5(
                bytes(sc.executive_person.get('name') + sc.executive_person.get('case_code'), encoding='utf-8'))
            sc.executive_person['id'] = executive_person_id
            ines(id=executive_person_id, path=_executive_person_total_path, data=sc.executive_person)
            ines(id=executive_person_id, path=_executive_person_gaoyuan_path, data=sc.executive_person)

if __name__ == '__main__':
    # 0表示未结构化   1成功结构化  2结构化出错  3缺少list或者detail 4表示es插入问题
    # logerror      100        200        300  301缺少detail         400

    item = {'url': 'http://sswy.hbsfgk.org:7080/pub/zxgk/detail.htm?bh=65CB639830304E645C17529A124A8D07&fy=100', 'list_response': '<Element tr at 0x7f4c6cd65098>', 'detail_response': '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\r\n<html xmlns="http://www.w3.org/1999/xhtml">\r\n<head>\r\n\t<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\r\n\t<meta charset="UTF-8">\r\n\t<title>被执行人耿月红详情-被执行人查询-诉讼无忧网</title>\r\n\t<script type="text/javascript">\r\n  var contextPath = "";\r\n  var theSessionId = "3C7CCC069A34C7E8013B4682C793CD72.sswy1";\r\n</script>\r\n<link rel="stylesheet" type="text/css" href="/jq/alerts/jquery.alerts.css">\r\n<link charset="utf-8" rel="stylesheet" type="text/css" href="/pub/V3/css/import.css" media="all" />\r\n<link charset="utf-8" rel="stylesheet" type="text/css" href="/pub/V3/css/variable_blue.css" media="all" />\r\n<link charset="utf-8" rel="stylesheet" type="text/css" href="/common/loading/css/loading.css" media="all" />\r\n<script type="text/javascript" src="/jq/jquery-1.8.3.js"></script>\r\n<script type="text/javascript" src="/common/js/handlebars-v4.0.5.js"></script>\r\n<script type="text/javascript" src="/jq/alerts/jquery.alerts.js"></script>\r\n<script type="text/javascript" src="/jq/jquery.json-2.4.js"></script>\r\n<script type="text/javascript" src="/jq/jquery.form.js"></script>\r\n<script type="text/javascript" src="/pub/comm.js"></script>\r\n<script type="text/javascript" src="/pub/V3/scripts/global.js"></script>\r\n<script type="text/javascript" src="/pub/lsfwpt/js/global.js"></script>\r\n<script type="text/javascript" src="/pub/V3/scripts/bootstrap-modal.js"></script>\r\n<script type="text/javascript" src="/common/loading/js/loading.js"></script>\r\n<script type="text/javascript" src="/pub/js/util/UUId.js"></script>\r\n<script type="text/javascript">\r\n  $.ajaxSetup({\r\n    contentType : "application/x-www-form-urlencoded;charset=utf-8",\r\n    complete : function(XMLHttpRequest, textStatus){\r\n      hideLoading();\r\n      var sessionstatus = XMLHttpRequest.getResponseHeader("sessionstatus"); \r\n      if(sessionstatus == "timeout"){\r\n        var loginUrl = XMLHttpRequest.getResponseHeader("loginUrl");\r\n        if (SSWY.isEmpty(loginUrl)) {\r\n          loginUrl = contextPath + "/login/pro.htm";\r\n        } else {\r\n          loginUrl = contextPath + loginUrl;\r\n        }\r\n        window.location.replace(loginUrl);\r\n      }\r\n    },\r\n    beforeSend : function(XMLHttpRequest, textStatus){\r\n    \tshowLoading("");\r\n    }\r\n  });\r\n  $.fn.pasteEvents = function( delay ) {\r\n      if (delay == undefined) delay = 20;\r\n      return $(this).each(function() {\r\n          var $el = $(this);\r\n          $el.on("paste", function() {\r\n              $el.trigger("prepaste");\r\n              setTimeout(function() { $el.trigger("postpaste"); }, delay);\r\n          });\r\n      });\r\n  };\r\n  \r\n  $.fn.setCursorPosition = function(option) {\r\n      var settings = $.extend({\r\n          index: 0\r\n      }, option)\r\n      return this.each(function() {\r\n          var elem  = this\r\n          var val   = elem.value\r\n          var len   = val.length\r\n          var index = settings.index\r\n   \r\n          // é\x9d\x9einputå\x92\x8ctextareaç\x9b´æ\x8e¥è¿\x94å\x9b\x9eÂ\x9e\r\n          var $elem = $(elem)\r\n          if (!$elem.is(\'input,textarea\')) return\r\n          // è¶\x85è¿\x87æ\x96\x87æ\x9c¬é\x95¿åº¦ç\x9b´æ\x8e¥è¿\x94å\x9b\x9eÂ\x9e\r\n          if (len < index) return\r\n   \r\n          setTimeout(function() {\r\n              elem.focus()\r\n              if (elem.setSelectionRange) { // æ\xa0\x87å\x87\x86æµ\x8fè§\x88å\x99¨\r\n                  elem.setSelectionRange(index, index)   \r\n              } else { // IE9-\r\n                  var range = elem.createTextRange()\r\n                  range.moveStart("character", -len)\r\n                  range.moveEnd("character", -len)\r\n                  range.moveStart("character", index)\r\n                  range.moveEnd("character", 0)\r\n                  range.select()\r\n              }\r\n          }, 10)\r\n      })\r\n  }\r\n  \r\n</script>\r\n\r\n<link rel="stylesheet" type="text/css" href="/newSfks/css/main.css" />\r\n<link rel="stylesheet" type="text/css" href="/newSfksImport/pub/css/znzs.css" />\r\n<script type="text/javascript" src="/newSfksImport/pub/js/xiaobao.js"></script>\r\n\r\n<c:set var="ctx" value="" />\r\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\r\n<html xmlns="http://www.w3.org/1999/xhtml">\r\n<head>\r\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\r\n<meta http-equiv="X-UA-Compatible" content="IE=edge" />\r\n</head>\r\n<style>\r\n.contentbox{\r\n\tbox-sizing: content-box;\r\n}\r\n</style>\r\n<body>\r\n\t<div id="sdXy_maskzs" class="sdxy_mask" style="display:none;"></div>\r\n\t<dl id="sdXy_boxzs" class="fd_dl_popup fd_dl_popup_dzsdxy sdxy_box"\r\n\t\tstyle="display:none;">\r\n\t\t<input type="text" id="zsSdId" value="" style="display:none">\r\n\t\t<dt class="dt_hd">\r\n\t\t\t<span class="sp_title">提示</span><a href="javascript:void(0);"\r\n\t\t\t\tonclick="closeZsSdxy()" class="popup_close">关闭</a>\r\n\t\t</dt>\r\n\t\t<dd class="dd_con">\r\n\t\t\t<div class="fd_form">\r\n\t\t\t\t<table class="fd_table_form_01 fd_table_form_07">\r\n\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t<h2 class="fd_h2_medium fd_align_center">电子送达协议</h2>\r\n\t\t\t\t\t\t<div class="fd_section_xz contentbox">\r\n\t\t\t\t\t\t\t<p id="zsSdxy_content"></p>\r\n\t\t\t\t\t\t</div>\r\n\t\t\t\t\t\t</div>\r\n\t\t\t\t\t</tr>\r\n\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t<td class="" colspan="2">\r\n\t\t\t\t\t\t\t<div class="fd_cell fd_cell_popup_btn contentbox">\r\n\t\t\t\t\t\t\t\t<a href="javascript:void(0);" class="fd_btn_small"\r\n\t\t\t\t\t\t\t\t\tonclick="downloadZsSdwj()"> <span class="sp_l"> <span\r\n\t\t\t\t\t\t\t\t\t\tclass="sp_r"> <span class="sp_m">同意</span>\r\n\t\t\t\t\t\t\t\t\t</span>\r\n\t\t\t\t\t\t\t\t</span>\r\n\t\t\t\t\t\t\t\t</a> <a href="javascript:void(0);" class="fd_btn_small_gray"\r\n\t\t\t\t\t\t\t\t\tonclick="closeZsSdxy()"> <span class="sp_l"> <span\r\n\t\t\t\t\t\t\t\t\t\tclass="sp_r"> <span class="sp_m">拒绝</span>\r\n\t\t\t\t\t\t\t\t\t</span>\r\n\t\t\t\t\t\t\t\t</span>\r\n\t\t\t\t\t\t\t\t</a>\r\n\t\t\t\t\t\t\t</div>\r\n\t\t\t\t\t\t</td>\r\n\t\t\t\t\t</tr>\r\n\t\t\t\t</table>\r\n\t\t\t</div>\r\n\t\t\t<!-- fd_p50_0 end -->\r\n\t\t</dd>\r\n\t\t<!-- dd_con end -->\r\n\t</dl>\r\n</body>\r\n</html>\r\n<script type="text/javascript">\r\n  var contextPath = "";\r\n</script>\r\n<!--小宇公大-->\r\n<div id="xiaobao-x" class="fd-baogong" style="display: none;">\r\n\t<div class="baogong-close" title="隐藏">关闭</div>\r\n\t<div class="mes-1-top"></div>\r\n\t<div class="mes-2-top"></div>\r\n\t<div class="baogong-bg">\r\n\t\t<p>\r\n\t\t\tHi，我是小宇~<br> \r\n\t\t\t欢迎使用<span id="fymc"></span>，\r\n\t\t\t有问题可点击问我！\r\n\t\t</p>\r\n\t</div>\r\n\t<div class="mes-1">\r\n\t\t<a>0</a> <b>消息（0）</b>\r\n\t</div>\r\n\t<div class="mes-2">\r\n\t\t<a>0</a> <b>待办（0）</b>\r\n\t</div>\r\n</div>\r\n<!--小宇公小-->\r\n<div class="fd-baogong-small" id="xiaobao-s"></div>\r\n<!--咨询小宇-->\r\n<div id="xiaobao" class="fd-consult-box">\r\n\t<div class="consult-head">\r\n\t\t<div class="logo">咨询小宇</div>\r\n\t\t<div class="link">\r\n\t\t\t<!-- <a class="fxpg">风险评估</a> \r\n\t\t\t<a class="zxsz">在线诉状</a> \r\n\t\t\t<a class="lacx">类案查询</a>\r\n\t\t\t<a class="flfg">法律法规</a> -->\r\n\t\t</div>\r\n\t\t<div class="close-btn"></div>\r\n\t</div>\r\n\t<div class="consult-body">\r\n\t\t<div class="left-nav">\r\n\t\t\t<ul class="js-left-nav">\r\n\t\t\t\t<li class="wd active">问答</li>\r\n\t\t\t\t<li class="db">待办<span>3</span></li>\r\n\t\t\t\t<li class="xx">消息<span>2</span></li>\r\n\t\t\t</ul>\r\n\t\t</div>\r\n\t\t<!--问答-->\r\n\t\t<div class="chat-box chat-box-wd active">\r\n\t\t\t<div class="chat-text">\r\n\t\t\t\t\r\n\t\t\t</div>\r\n\t\t\t<div class="chat-input">\r\n\t\t\t\t<textarea placeholder="诉状不会写，网站不会操作，想了解案件进展都可以咨询小宇哦~" name=""\r\n\t\t\t\t\tid="content" rows="" cols=""></textarea>\r\n\t\t\t\t<button class="send" style="cursor:pointer;">发送</button>\r\n\t\t\t</div>\r\n\t\t</div>\r\n\t\t<!--代办-->\r\n\t\t<div class="chat-box chat-box-db">\r\n\t\t\t<div class="chat-text">\r\n\t\t\t\t\r\n\t\t\t</div>\r\n\t\t</div>\r\n\t\t<!--消息-->\r\n\t\t<div class="chat-box chat-box-xx">\r\n\t\t\t<div class="chat-text">\r\n\t\t\t\r\n\t\t\t\t\r\n\t\t\t</div>\r\n\t\t\t<div class="chat-input-empty">\r\n\t\t\t\t<button class="empty" onclick="readAllxx();">全部清空</button>\r\n\t\t\t</div>\r\n\t\t</div>\r\n\t\t<!-- 顶部连接的div 临时 -->\r\n\t\t<div class="chat-box chat-bdgn">\r\n\t\t\t<div class="chat-text">\r\n\t\t\t\t\t此功能正在开发中，敬请期待...\r\n\t\t\t</div>\r\n\t\t</div>\r\n\t</div>\r\n</div>\r\n\t<script type="text/javascript">\r\n\tvar courtId = \'100\';\r\n\tvar bzxrid = \'65CB639830304E645C17529A124A8D07\';\r\n\tvar fyid = \'100\';\r\n\tfunction xsjb(){\r\n\t\tvar url = contextPath + "/pub/zxxsjb/jbxz.htm?bzxrid=" + bzxrid + "&fy=" + courtId;\r\n\t\twindow.open(url);\r\n\t};\r\n\t</script>\r\n</head>\r\n<body>\r\n<div class="contain fd_contain_noimg">\r\n\t<header class="header">\r\n  <div class="header_shadow">\r\n    <div class="header_in">\r\n      \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n<div class="header_t_bg">\r\n<div class="header_t">\r\n  <a href="http://hbgy.hbsfgk.org" title="河北省高级人民法院">返回网站首页</a>\r\n  \r\n    \r\n      <span class="sp_load_prev">\r\n\t\r\n\t\r\n        <a href="/login/pro.htm?fy=100" class="a_load">登录</a>\r\n\t\r\n\r\n\t\r\n        <a href="/login/register.htm?fy=100" class="a_register">注册</a>\r\n\t\r\n\r\n      </span>\r\n    \r\n    \r\n  \r\n</div>\r\n</div><div class="header_m">\r\n\t<a href="http://hbgy.hbsfgk.org" title="河北省高级人民法院" class="logo"><img src="/pub/V3/images/logo.png" alt="logo" />河北省高级人民法院</a>\r\n</div>\r\n</div>\r\n  </div>\r\n</header>\r\n  <div class="fd_m_auto fd_width_1000"><h2 class="fd_h2_bnav"><a href="http://hbgy.hbsfgk.org">首页</a><span class="fd_separate">></span><a href="/fymh/100/zxgk.htm">执行公开</a><span class="fd_separate">></span><span class="current_location">详情</span></h2></div>\r\n\r\n\t<article class="content">\r\n\t\t<div class="main">\r\n\t\t\t\r\n\t\t\t\t\r\n\t\t\t\t\t<dl class="dl_01 dl_01_no_shadow dl_01_no_bd dl_01_no_bg">\r\n\t\t\t\t\t\t<dt class="dt_hd dt_have_bd">\r\n\t\t\t\t\t\t\t<span class="sp_title">限制高消费</span>\r\n\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t</dt>\r\n\t\t\t\t\t\t<dd class="dd_con">\r\n\t\t\t\t\t\t\t<table class="fd_table_02">\r\n\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t<tr class="tr_first" >\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_first fd_width_fix_250"><div class="td_cell">诉讼地位</div></td>\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_last"><div class="td_cell">\r\n\t\t\t\t\t\t\t\t\t\t被执行人</div>\r\n\t\t\t\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t<tr  >\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_first "><div class="td_cell">被执行人姓名/名称</div></td>\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_last"><div class="td_cell">\r\n\t\t\t\t\t\t\t\t\t\t耿月红</div>\r\n\t\t\t\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t<tr  >\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_first "><div class="td_cell">被执行人类型</div></td>\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_last"><div class="td_cell">\r\n\t\t\t\t\t\t\t\t\t\t自然人</div>\r\n\t\t\t\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t<tr  >\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_first "><div class="td_cell">证件类型</div></td>\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_last"><div class="td_cell">\r\n\t\t\t\t\t\t\t\t\t\t中华人民共和国居民身份证</div>\r\n\t\t\t\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t<tr  >\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_first "><div class="td_cell">证件号码</div></td>\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_last"><div class="td_cell">\r\n\t\t\t\t\t\t\t\t\t\t1305341974****0022</div>\r\n\t\t\t\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t<tr  >\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_first "><div class="td_cell">被执行人性别</div></td>\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_last"><div class="td_cell">\r\n\t\t\t\t\t\t\t\t\t\t女</div>\r\n\t\t\t\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t<tr  >\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_first "><div class="td_cell">被执行人年龄</div></td>\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_last"><div class="td_cell">\r\n\t\t\t\t\t\t\t\t\t\t42</div>\r\n\t\t\t\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t<tr  >\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_first "><div class="td_cell">限制原因</div></td>\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_last"><div class="td_cell">\r\n\t\t\t\t\t\t\t\t\t\t拒不履行判决书义务</div>\r\n\t\t\t\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t<tr  >\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_first "><div class="td_cell">限制内容</div></td>\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_last"><div class="td_cell">\r\n\t\t\t\t\t\t\t\t\t\t限制高消费</div>\r\n\t\t\t\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t<tr  >\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_first "><div class="td_cell">限制开始日期</div></td>\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_last"><div class="td_cell">\r\n\t\t\t\t\t\t\t\t\t\t2017-12-26</div>\r\n\t\t\t\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t<tr  >\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_first "><div class="td_cell">案号</div></td>\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_last"><div class="td_cell">\r\n\t\t\t\t\t\t\t\t\t\t（2017）冀0534执448号</div>\r\n\t\t\t\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t<tr  >\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_first "><div class="td_cell">立案日期</div></td>\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_last"><div class="td_cell">\r\n\t\t\t\t\t\t\t\t\t\t2017-07-31</div>\r\n\t\t\t\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t<tr  >\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_first "><div class="td_cell">执行法院</div></td>\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_last"><div class="td_cell">\r\n\t\t\t\t\t\t\t\t\t\t清河县人民法院</div>\r\n\t\t\t\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t<tr  >\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_first "><div class="td_cell">案件状态</div></td>\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_last"><div class="td_cell">\r\n\t\t\t\t\t\t\t\t\t\t审理</div>\r\n\t\t\t\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t<tr  >\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_first "><div class="td_cell">执行依据文书编号</div></td>\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_last"><div class="td_cell">\r\n\t\t\t\t\t\t\t\t\t\t（2017）冀0534民初271号</div>\r\n\t\t\t\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t<tr  >\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_first "><div class="td_cell">经办机构（做出执行依据单位）</div></td>\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_last"><div class="td_cell">\r\n\t\t\t\t\t\t\t\t\t\t清河县人民法院</div>\r\n\t\t\t\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t<tr  >\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_first "><div class="td_cell">发布日期</div></td>\r\n\t\t\t\t\t\t\t\t\t<td class="td_data_row td_data_last"><div class="td_cell">\r\n\t\t\t\t\t\t\t\t\t\t2017-12-26</div>\r\n\t\t\t\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t</table>\r\n\t\t\t\t\t\t\t<!-- fd_table_02 end -->\r\n\t\t\t\t\t\t</dd>\r\n\t\t\t\t\t</dl>\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t\r\n\t\t</div>\r\n\t\t<!-- main end -->\r\n\t</article>\r\n\t<!-- content end -->\r\n\t<footer class="footer">\r\n  <div class="footer_in">技术支持：北京华宇信息技术有限公司</div>\r\n</footer>\r\n</div>\r\n</body>\r\n</html>', 'data_path': '河北省高级人民法院网-执行信息-限制高消费人'}
    run(item)
