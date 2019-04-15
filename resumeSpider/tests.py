from django.test import TestCase

# Create your tests here.
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

url = 'https://jobs.zhaopin.com/CC689935929J00119268912.htm'

res = requests.get(url)
res.encoding = 'utf-8'
html = res.text

soup = BeautifulSoup(html, 'lxml')

# contents = soup.find_all('div', attrs={'class','intro-content'})[0]
# cont = contents.find_all('div')

contents = soup.find_all('div', attrs={'class': 'pos-ul'})[0]
pos_content = contents.find_all('p') # 获取到一个列表
list_con = []
for con in pos_content:
    list_con.append(con.get_text().strip())

print(list_con)


