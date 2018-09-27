import requests
import re
from lxml import etree
import pymysql
from bs4 import BeautifulSoup
import time
from pyquery import PyQuery as pq
#先定义一个login类，初始化一些变量：
class Login(object):
    def __init__(self):
        self.headers = {
            'Referer':'http://www.bidchance.com/freesearch.do?&filetype=&channel=zhongbiao&currentpage=1&searchtype=zb&queryword=&displayStyle=title&pstate=&field=all&leftday=&province=&bidfile=&project=&heshi=&recommend=&field=all&jing=&starttime=&endtime=&attachment=',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
            'Host':'www.bidchance.com'
        }
        self.login_url = 'http://www.bidchance.com/homePageUc.do' #最初的登陆界面
        self.post_url = 'http://www.bidchance.com/logon.do'
        self.logined_url = 'http://www.bidchance.com/homePageUc.do'
        self.aim_url = 'http://www.bidchance.com/search.do?channel=zhongbiao&searchtype=zb&province=&channel=gonggao&queryword=&searchtype=zb&bidfile=&recommend=&leftday=&searchyear=&field=all&displayStyle=title&attachment=&starttime=&endtime=&pstate='
        self.session = requests.Session()
    #获取cookie
    def token(self):
        response = self.session.get(self.login_url,headers = self.headers)

    def login(self,userid,password):
        post_data = {
            'userid' : userid,
            'pwd' : password,
            'submit': '%B5%C7%C2%BC'
        }
        response = self.session.post(self.post_url,data = post_data,headers=self.headers)
        if response.status_code == 200:
            response = self.session.get(self.aim_url,headers = self.headers)
            href = re.compile(r'&id=(.*?)&q="', re.S).findall(response.text)
        for i in range(len(href)):
            url = 'http://www.bidchance.com/info.do?channel=zhongbiao&id=' + href[i] + '&q='
            response = self.session.get(url,headers = self.headers)
            tupple = self.findlly_url(response.text,url)
            self.sql(tupple)
            print('成功')
    def sql(self,tupple):
        config = {
            'host': '10.1.5.160',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'database': 'histroy',
            'charset': 'utf8mb4'
        }

        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        # print(1,dict['截止日期'])
        sql = 'insert into hist2(url,create_time,html,source,title,publish_data,lables,body,head,招标编号,采购业主,招标公司,联系人,联系电话,通讯地址,邮政编码,截止日期,加入日期,所属地区) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'  # 编写sql语句
        cursor.execute(sql,tupple)

        # cursor.execute(sql, (result[i][0], creat_time, req,source,title,publish_data,lables,str(body)))  # 执行sql语句
        #data = cursor.fetchall()
        print(tupple)

        conn.commit()  # 提交事务
    def findlly_url(self,html,url):
        soup = BeautifulSoup(html, 'html.parser')
        a = soup.find_all('div', attrs={'class': 'xlbodybox', 'id': "infocontent"})  # 正文内容，表格也在里面
        b = soup.find_all('div', attrs={'class': 'xllabel-l'})
        creat_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        source = '招标网'
        try:
            p = pq(html)
            title = p('div#infotitle').text()
        except:
            title = ''
        #print(title)
        try:
            publish_data = re.compile('发布日期：(.*?日)', re.S).findall(str(b[0]))[0]
        except:
            publish_data = ''
        #print(publish_data)
        try:
            lables = re.compile('title="(.*?)"', re.S).findall(str(b[0]))[0]
        except:
            lables = ''
        #print(lables)
        dict = {}
        p = pq(html)
        doc = p('table#infotablecontent > tr > *')
        list = ['招标编号', '采购业主', '招标公司', '联系人', '联系电话', '通讯地址', '邮政编码', '截止日期', '加入日期', '所属地区']
        for k in range(0, len(doc) - 1, 2):
            try:
                dict[doc[k].text] = doc[(k + 1)].text
            except:
                break
        for y in list:
            if y not in dict.keys():
                dict[y] = ''
            else:
                pass
        #print(dict)
        try:
            p = pq(html)
            body = p('dd#infohtmlcon > *').text()
        except:
            body = ''
        #print(body)
        return (url,creat_time, html, source, str(title),str(publish_data), str(lables), str(body), str(doc.text()),dict['招标编号'],dict['采购业主'],dict['招标公司'],dict['联系人'],dict['联系电话'],dict['通讯地址'],dict['邮政编码'],dict['截止日期'],dict['加入日期'],dict['所属地区'])


login = Login()
login.login(userid='yscredit',password='youshu808')