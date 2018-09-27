# coding:utf-8
import time
import requests
from urllib.parse import urlparse
import json
from datetime import datetime
import threading
from copy import copy


class ESman:
    def __init__(self, url: str):
        """
        Args
            url: http://10.1.1.28:9200/judge_doc/total_doc
        """
        self.url = url
        self.in_time = 3
        self.in_num = 1
        self.stop_time = 5
        self.datas = []
        self.in_last = time.time()
        parse = urlparse(url)
        self._index, self._type = parse.path[1:].split('/')
        self.url_host = 'http://' + parse.netloc

        run_thread = threading.Thread(target=self.run)
        run_thread.daemon = True
        run_thread.start()



    def run(self):
        while True:
            time.sleep(0.5)
            self.run_once()


    def run_once(self):
        print('{}, exists record:{}, interval time:{}'.format(datetime.now().isoformat(), len(self.datas), time.time()-self.in_last))
        if len(self.datas) >= self.in_num:
            self.ines_many()
        if time.time() - self.in_last >= self.in_time and len(self.datas) > 0:
            self.ines_many()


    def ines_many(self):
        in_strs = ''
        for data in self.datas:
            _data = copy(data)
            print(_data)
            _id = _data['_id']
            del _data['_id']
            action_dict = {"index": {"_index": self._index, "_type": self._type, "_id": _id}}
            request_body_dic = _data
            in_str = '{action}\n{request_body}\n'.format(action=json.dumps(action_dict), request_body=json.dumps(request_body_dic))
            in_strs += in_str
        response = requests.post(self.url_host+'/_bulk', data=in_strs.encode('utf-8'))
        print(response.text)
        print('{}, succeed insert record: {}'.format(datetime.now().isoformat(), len(self.datas)))
        self.datas = []
        self.in_last = time.time()


    def ines(self, data):
        """
        Args
            data: {'_id': _id}
        """
        self.datas.append(data)
        time.sleep(2)

if __name__ == '__main__':
    data = {'title': '测试1', '_id': 'test1'}
    esman = ESman('http://10.1.1.28:9200/judge_doc/total_doc')
    esman.ines(data)
    data = {'title': '测试1', '_id': 'test1'}
    time.sleep(5)
    esman.ines(data)

