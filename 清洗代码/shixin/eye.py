import os
import sys
sys.path.append(os.path.abspath(__file__ + "/../../../"))
from IKEA.mysql.mysqlbase import MysqlBase
from IKEA.shixin.config import connecter as connecter
import requests
from datetime import date
from datetime import timedelta


def robot(content):
    data = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }
    page = requests.post(
        'https://oapi.dingtalk.com/robot/send?access_token=ed2a4f043112a17e542d226e551b58aa4dc4a0399a4701465553ece93429dd49',
        json=data)
    return page.text


yesterday = (date.today() - timedelta(days=1)).isoformat()
mb = MysqlBase(connecter)
table = 'zhixing_no_detail'
j = {
    "msgtype": "text",
    "text": {"content": ""}
}
content = ''
for items in mb._execute("select `data_path` ,count(`data_path` ) as c from `{}`  group by `data_path` ".format(table)):
    data_path = items['data_path']
    total = items['c']

    for num in mb._execute("select count(*) as c from {} where create_time>'{}' and data_path='{}'".format(table, '2017-08-30', data_path)):
        content = content + '{} {} {}\n'.format(data_path, num['c'], total)
robot(content)


