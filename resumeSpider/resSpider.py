#用于爬取智联公司招聘信息
import requests
import json
import time
from lxml import etree
from bs4 import BeautifulSoup
#多线程爬虫
from threading import Thread
from multiprocessing import Queue
import urllib

#存储到数据库
import pymysql


class ZhilianSpider(object):
    def __init__(self):
        self.headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
        #url队列
        self.urlQueue = Queue()
        #解析队列
        self.parseQueue = Queue()
        #数据库
        self.db = pymysql.connect('127.0.0.1', 'root', 'ake123456', 'MyResume', charset='utf8')
        self.cursor = self.db.cursor()

    def getPageurl(self):
        '''获取 url'''
        baseurl = 'https://fe-api.zhaopin.com/c/i/sou?'
        for page in range(0, 720, 90):
            time.sleep(1)
            params ={
                'start': page,
                'pageSize': 90,
                'cityId': 653,
                'workExperience': -1,
                'education': -1,
                'companyType': -1,
                'employmentType': -1,
                'jobWelfareTag': -1,
                'kw': 'python开发',
                'kt': 3,
                '_v': 0.25103539,
                'x - zp - page - request - id': '544d1215f4154ef6b9edf8ea4db5247c - 1552718257449 - 980370'
            }

            res = requests.get(baseurl, params=params, headers=self.headers)
            res.encoding = 'utf-8'
            resStr = res.text
            jsStr = json.loads(resStr)
            company_urls = jsStr['data']['results']
            for company_url in company_urls:
                positionURL = company_url['positionURL']
                print(positionURL)
                #入队列

                #数据存到 posbrief表中
                res = self.saveposbrief(company_url)
                if res is False:
                    continue
                    # self.urlQueue.put(positionURL)    #如果需要全部更新数据，去掉这条的注释，continue 加上注释
                else:
                    self.urlQueue.put(positionURL)


    def getHTML(self):
        '''处理数据入队列'''
        while True:
            print('开始获取 url')
            if not self.urlQueue.empty():
                #从队列中获取 url
                posiurl = self.urlQueue.get()
                res = requests.get(posiurl, headers=self.headers)
                res.encoding = 'utf-8'
                html = res.text
                #将 html 文本放入队列
                self.parseQueue.put((html, posiurl))
            else:
                break

    def savePage(self):
        '''解析数据'''
        listdata = []
        while True:
            print('开始解析数据')
            if not self.parseQueue.empty():
                #从队列中获取数据解析
                html, posiurl = self.parseQueue.get()

                soup = BeautifulSoup(html, 'lxml')
                try:
                    contents = soup.find_all('div', attrs={'class': 'pos-ul'})[0]
                    pcontents = contents.find_all('p')  # 获取到一个列表
                    pcontents += contents.find_all('div')
                    listcon = []
                    for con in pcontents:
                        listcon.append(con.get_text().strip())
                except IndexError:
                    contents = '略'
                    listcon =[]
                    listcon.append(contents)


                brief = soup.find_all('div', attrs={'class': 'jjtxt'})
                bright = soup.find_all('div', attrs={'class':'pos-info-tit'})
                try:
                    pos_brief = brief[0].get_text()
                except:
                    pos_brief = '略'
                #职位亮点
                try:
                    pos_bright = bright[0].get_text()
                except:
                    pos_bright = '略'
                #创建解析对象
                parseHTML = etree.HTML(html)
                data = {}
                data['positionUrl'] = posiurl
                data['title'] = parseHTML.xpath('//div[@class="new-info"]/ul/li/h1/text()')[0]
                data['salary'] = parseHTML.xpath('//div[@class="new-info"]/ul/li/div/strong/text()')[0]
                data['company'] = parseHTML.xpath('//div[@class="new-info"]/ul/li/div/a/text()')[0]
                try:
                    data['address'] = parseHTML.xpath('//p[@class="add-txt"]/text()')[0]  # 公司地址
                except:
                    data['address'] = '略'
                data['company_brief'] = pos_brief.strip()    #公司描述
                data['content'] = str(listcon)  # 职位描述
                data['bright'] = pos_bright.strip()  #职位亮点
                #存储
                print('ok')
                self.savesql(data)
            else:
                break

    def savesql(self, data):
        '''保存详细信息到数据库'''
        sel = "select * from Positions where pos_url_id ='%s';" % data['positionUrl']
        self.cursor.execute(sel)
        res_sel = self.cursor.execute(sel)
        if res_sel:
            print('这条数据已存在,更新数据')
            upd = "update Positions set pos_title = %s, pos_salary = %s, pos_company = %s, pos_address = %s, pos_company_brief = %s,  pos_content = %s, pos_bright = %s where pos_url_id = %s"
            L = [data['title'], data['salary'], data['company'], data['address'], data['company_brief'],
                 data['content'], data['bright'], data['positionUrl']]
            self.cursor.execute(upd, L)
            self.db.commit()
            print('数据更新成功')
        else:
            ins = "insert into Positions(pos_title, pos_salary, pos_company, pos_address, pos_company_brief,  pos_content, pos_bright, pos_url_id) values(%s, %s, %s, %s, %s, %s, %s, %s)"  #检查这里
            L = [data['title'], data['salary'], data['company'], data['address'], data['company_brief'], data['content'], data['bright'], data['positionUrl']]
            self.cursor.execute(ins, L)
            self.db.commit()    #提交到数据库
            print('保存')

    def saveposbrief(self, company_url):
        '''保存简介内容到数据库'''
        sel = "select * from Posbrief where positionURL = '%s'" % company_url['positionURL']
        self.cursor.execute(sel)
        data_sel = self.cursor.fetchone()
        if data_sel:
            print('brief数据已存在')
            return False    #数据已存在
        else:
            ins = "insert into Posbrief values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            try:
                businessArea = company_url['businessArea']
            except:
                businessArea = '无'

            L = [businessArea, company_url['createDate'], company_url['jobName'], company_url['positionURL'], company_url['salary'], company_url['updateDate'], str(company_url['company']), company_url['companyLogo'], str(company_url['eduLevel']), str(company_url['jobTag']), str(company_url['jobType'])]
            #company_url['businessArea']有可能没有 需要处理异常
            self.cursor.execute(ins, L)
            self.db.commit()
            print('简介表插入')


    def workOn(self):
        '''启动程序'''
        self.getPageurl()

        t1list = []
        t2list = []

        #采集url线程
        for i in range(5):
            t = Thread(target=self.getHTML())
            t1list.append(t)
            t.start()

        for j in t1list:
            j.join()

        #保存线程
        for x in range(5):
            t = Thread(target=self.savePage())
            t2list.append(t)
            t.start()

        for y in t2list:
            y.join()
