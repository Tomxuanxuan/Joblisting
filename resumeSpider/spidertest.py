#用于爬取公司招聘信息
import requests
import json
import time
from lxml import etree
import re
from bs4 import BeautifulSoup
#多线程爬虫
from threading import Thread
from multiprocessing import Queue
import urllib

#存储到数据库
import pymysql

baseurl = 'https://jobs.zhaopin.com/CC629585921J00276382907.htm'
res = requests.get(baseurl)
res.encoding = 'utf-8'
html = res.text

p = re.compile('<div class="intro-content">\n<div>.*?<span.*?>(.*?)</span>.*?<div>(.*?)</div><div>(.*?)<br></div>')
r1 = p.findall(html)
print(r1)

soup = BeautifulSoup(html, 'lxml')
content = soup.find_all('div', attrs={'class':'pos-ul'})
brief = soup.find_all('div', attrs={'class':'jjtxt'})
pos_brief = brief[0].get_text()
pos_content = content[0].get_text()


data = {}
parseHTML = etree.HTML(html)
data['title'] = parseHTML.xpath('//div[@class="new-info"]/ul/li/h1/text()')[0]
data['salary'] = parseHTML.xpath('//div[@class="new-info"]/ul/li/div/strong/text()')[0]
data['company'] = parseHTML.xpath('//div[@class="new-info"]/ul/li/div/a/text()')[0]
data['address'] = parseHTML.xpath('//p[@class="add-txt"]/text()')[0]  # 公

data['company_brief'] = pos_brief  #公司描述
data['content'] = pos_content  # 职位描述


# print(data)
