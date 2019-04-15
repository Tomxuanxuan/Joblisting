from django.shortcuts import render,HttpResponse,redirect
from .models import *
import json
import math
import datetime
from django.db.models import Count      #导入 count 用来聚合查询地址数量

from django.db.models import Q
from .resSpider import ZhilianSpider

#pandas读取数据库
from sqlalchemy import create_engine
import pandas
import numpy

#留言板
from resume.models import Contact

def JobIndex(request):
    '''主页'''
    if request.method == 'GET':
        #分页功能
        pagesize = 20   #每页显示20条数据
        first_page = 1
        page = request.GET.get('page', '1') #获取页数，默认为1
        page = int(page)
        count = Posbrief.objects.all().count()
        last_page = math.ceil(count / pagesize)    #向上取整，得到页数
        if page == 1:
            prev_page = 1
        else:
            prev_page = page - 1    #上一页

        if page == last_page:
            next_page = last_page   #尾页 这里还要传递个标志过去，修改前端 css
        else:
            next_page = page + 1

        # [: 30]
        # jobbrief = Posbrief.objects.all().order_by(Posbrief.updateDate)
        jobbrief = Posbrief.objects.all()[(page - 1) * pagesize:page * pagesize]
    else:
        # 跳转页面
        page = int(request.POST.get('page'))

        pagesize = 20
        count = Posbrief.objects.all().count()
        last_page = math.ceil(count / pagesize)  # 向上取整，得到页数
        prev_page = page + 1
        if page > last_page:
            page = last_page
            prev_page = last_page
        if page <= 0:
            page = 1
        jobbrief = Posbrief.objects.all()[(page - 1) * pagesize:page * pagesize]

    list_brief = []
    for brief in jobbrief:
        dic_brief = {}
        dic_brief['businessArea'] = brief.businessArea
        dic_brief['jobName'] = brief.jobName
        dic_brief['salary'] = brief.salary
        dic_brief['updateDate'] = brief.updateDate
        dic_brief['createDate'] = brief.createDate
        urlid = brief.positionURL.split('/')[-1]    #412944836250004.htm
        dic_brief['positionURL'] = urlid
        dic_brief['companyLogo'] = brief.companyLogo
        jobTag = eval(brief.jobTag)['searchTag'].split(',')   #['五险一金', '绩效奖金', '通讯补助', '弹性工作', '定期体检', '员工旅游', '高温补贴', '节日福利']
        dic_brief['jobTag'] = jobTag
        jobType = brief.jobType.split('\'')[3]
        dic_brief['jobType'] = jobType
        #{'number': 'CZ427070510', 'size': {'code': '3', 'name': '100-499人'}, 'name': '杭州联众医疗科技股份有限公司', 'type': {'code': '9', 'name': '上市公司'}, 'url': 'http.com/CZ427070510.htm'}
        company = eval(brief.company)
        dic_brief['companyname'] = company['name']
        dic_brief['companysize'] = company['size']['name']
        dic_brief['companytype'] = company['type']['name']
        list_brief.append(dic_brief)

    #侧边栏数据
    dic_slidebar = {}
    dic_slidebar['pydevelop'] = Posbrief.objects.filter(jobName__contains='python开发').count()
    dic_slidebar['develop'] = Posbrief.objects.filter(jobName__contains='开发').count()
    dic_slidebar['operation'] = Posbrief.objects.filter(jobName__contains='运维').count()
    dic_slidebar['test'] = Posbrief.objects.filter(jobName__contains='测试').count()
    dic_slidebar['artificialintelligence'] = Posbrief.objects.filter(jobName__contains='人工智能').count()
    dic_slidebar['largedata'] = Posbrief.objects.filter(jobName__contains='大数据').count()
    dic_slidebar['product'] = Posbrief.objects.filter(jobName__contains='产品').count()
    dic_slidebar['others'] = Posbrief.objects.exclude(
        Q(jobName__contains='开发') | Q(jobName__contains='运维') | Q(jobName__contains='测试') | Q(
            jobName__contains='人工智能') | Q(jobName__contains='大数据') | Q(jobName__contains='产品')).count()

    addressNoOrder = Posbrief.objects.values('businessArea').annotate(count=Count('*'))      #聚合查询地址与对应的数量

    addressNum = addressNoOrder.order_by('count').reverse()      #按照数量排序，默认为升序，reverse 反转为降序排列




    return render(request, 'category.html', locals())



def Search(request):
    if request.method == 'GET':
        key = request.GET.get('search')
        print(key)
    else:
        key = request.POST.get('search')
        # 直接搜索，不选择类型与地址， 一个参数

    if key:
        listkey = key.strip().split(' ')
        if len(listkey) == 1 and key != 'other':
            position = listkey[0].strip()
            #查询结果
            positions = Posbrief.objects.filter(jobName__contains=position)   #名称区分大小写的包含搜索结果
        elif len(listkey) == 1 and key == 'other':
            positions = Posbrief.objects.exclude(
                Q(jobName__contains='开发') | Q(jobName__contains='运维') | Q(jobName__contains='测试') | Q(
                    jobName__contains='人工智能') | Q(jobName__contains='大数据') | Q(jobName__contains='产品'))

        else:
            position = listkey[0].strip()
            address = listkey[-1].strip()
            positions = Posbrief.objects.filter(Q(jobName__contains=position) & Q(businessArea__contains=address))



        # 分页功能
        flag = 'search' #前端接收这个标志，表名是搜索的内容的分页
        pagesize = 20  # 每页显示20条数据
        first_page = 1

        page = request.GET.get('page', '1')  # 获取页数，默认为1
        page = int(page)
        count = positions.count()   #获取到查询的数量
        last_page = math.ceil(count / pagesize)  # 向上取整，得到页数
        if page == 1:
            prev_page = 1
        else:
            prev_page = page - 1  # 上一页
        if page == last_page:
            next_page = last_page  # 尾页 这里还要传递个标志过去，修改前端 css
        else:
            next_page = page + 1
        # [: 30]
        jobbrief = positions[(page - 1) * pagesize:page * pagesize] #切片



        list_brief = []
        for brief in jobbrief:
            dic_brief = {}
            dic_brief['businessArea'] = brief.businessArea
            dic_brief['jobName'] = brief.jobName
            dic_brief['salary'] = brief.salary
            dic_brief['updateDate'] = brief.updateDate
            dic_brief['createDate'] = brief.createDate
            urlid = brief.positionURL.split('/')[-1]  # 412944836250004.htm
            dic_brief['positionURL'] = urlid
            dic_brief['companyLogo'] = brief.companyLogo

            jobTag = eval(brief.jobTag)['searchTag'].split(
                ',')  # ['五险一金', '绩效奖金', '通讯补助', '弹性工作', '定期体检', '员工旅游', '高温补贴', '节日福利']
            dic_brief['jobTag'] = jobTag

            jobType = brief.jobType.split('\'')[3]
            dic_brief['jobType'] = jobType
            # {'number': 'CZ427070510', 'size': {'code': '3', 'name': '100-499人'}, 'name': '杭州联众医疗科技股份有限公司', 'type': {'code': '9', 'name': '上市公司'}, 'url': 'http.com/CZ427070510.htm'}

            company = eval(brief.company)
            dic_brief['companyname'] = company['name']
            dic_brief['companysize'] = company['size']['name']
            dic_brief['companytype'] = company['type']['name']
            list_brief.append(dic_brief)

    dic_slidebar = {}
    dic_slidebar['pydevelop'] = Posbrief.objects.filter(jobName__contains='python开发').count()
    dic_slidebar['develop'] = Posbrief.objects.filter(jobName__contains='开发').count()
    dic_slidebar['operation'] = Posbrief.objects.filter(jobName__contains='运维').count()
    dic_slidebar['test'] = Posbrief.objects.filter(jobName__contains='测试').count()
    dic_slidebar['artificialintelligence'] = Posbrief.objects.filter(jobName__contains='人工智能').count()
    dic_slidebar['largedata'] = Posbrief.objects.filter(jobName__contains='大数据').count()
    dic_slidebar['product'] = Posbrief.objects.filter(jobName__contains='产品').count()
    dic_slidebar['others'] = Posbrief.objects.exclude(
        Q(jobName__contains='开发') | Q(jobName__contains='运维') | Q(jobName__contains='测试') | Q(
            jobName__contains='人工智能') | Q(jobName__contains='大数据') | Q(jobName__contains='产品')).count()

    return render(request, 'category.html', locals())

def JobSingle(request):
    positionurl = request.GET.get('job')
    resurl = 'https://jobs.zhaopin.com/' + positionurl
    job = Positions.objects.get(pos_url=resurl)
    jobbrief =Posbrief.objects.get(positionURL=resurl)
    lise_pos = []
    dic_job = {}
    dic_job['businessAre'] =  jobbrief.businessArea
    dic_job['createDate'] = jobbrief.createDate
    dic_job['jobName'] = jobbrief.jobName
    dic_job['updateDate'] = jobbrief.updateDate
    dic_job['companyLogo'] = jobbrief.companyLogo
    company = eval(jobbrief.company)
    dic_job['companyname'] = company['name']

    jobTag = jobbrief.jobTag.split('\'')[-2]
    dic_job['jobTag'] = jobTag
    jobType = jobbrief.jobType.split('\'')[3]
    dic_job['jobType'] = jobType

    dic_job['pos_url'] = job.pos_url
    dic_job['pos_title'] = job.pos_title
    dic_job['pos_salary'] = job.pos_salary
    dic_job['pos_company'] = job.pos_company
    dic_job['pos_address'] = job.pos_address
    dic_job['pos_company_brie'] = job.pos_company_brief
    dic_job['pos_content'] = eval(job.pos_content)

    poscontent = eval(job.pos_content)

    dic_job['pos_bright'] = job.pos_bright

    dic_slidebar = {}
    dic_slidebar['pydevelop'] = Posbrief.objects.filter(jobName__contains='python开发').count()
    dic_slidebar['develop'] = Posbrief.objects.filter(jobName__contains='开发').count()
    dic_slidebar['operation'] = Posbrief.objects.filter(jobName__contains='运维').count()
    dic_slidebar['test'] = Posbrief.objects.filter(jobName__contains='测试').count()
    dic_slidebar['artificialintelligence'] = Posbrief.objects.filter(jobName__contains='人工智能').count()
    dic_slidebar['largedata'] = Posbrief.objects.filter(jobName__contains='大数据').count()
    dic_slidebar['product'] = Posbrief.objects.filter(jobName__contains='产品').count()
    dic_slidebar['others'] = Posbrief.objects.exclude(
        Q(jobName__contains='开发') | Q(jobName__contains='运维') | Q(jobName__contains='测试') | Q(
            jobName__contains='人工智能') | Q(jobName__contains='大数据') | Q(jobName__contains='产品')).count()


    return render(request, 'single.html', locals())

def UpdateJobs(request):
    '''调取爬虫更新工作数据'''
    zhilian = ZhilianSpider()
    zhilian.workOn()
    print('执行完毕')
    return redirect('/job')

def Analyze(request):
    '''处理数据分析'''
    if request.session.get('user_id') != 1:
        return redirect('/resume/login')
    else:
        #连接数据库
        engine = create_engine('mysql+mysqldb://root:ake123456@localhost:3306/MyResume')
        select_statement = 'select businessArea, jobName, salary, eduLevel, jobType from Posbrief'
        res = pandas.read_sql(sql=select_statement, con=engine)

        # res_aaa = res[['salary']].groupby(['businessArea'], as_index=False).count()
        # print(res_aaa)
        # print(res.loc['西湖'])
        #每个区域的工作数量
        select_businessArea = "select businessArea,count(businessArea) from Posbrief group by businessArea"
        res_area = pandas.read_sql(sql=select_businessArea, con=engine)
        #转为字典 {'xx':{'xx':123, 'xx':234,...}}
        res_area.rename(columns={'count(businessArea)':'areaNum'}, inplace=True)
        dict_res_area = res_area.to_dict('int')
        list_area = []
        #{0: {'businessArea': '西湖', 'areaNum': 45}, 1: {'businessArea': '浦沿', 'areaNum': 13}
        for index in dict_res_area:
            list_area.append(dict_res_area[index])  #这是转化为列表字典的区域工作数量



        def dealmoney(sel_info, name, posnum):
            '''定义薪资情况'''
            money_dict = {}

            salary_lists = sel_info.salary
            salary_list = []
            for x in salary_lists:
                if x != '薪资面议':
                    salary_list.append(x)

            # 去掉薪资面议的行
            money_info = sel_info[sel_info.salary.isin(salary_list)]

            # 对薪资字符进行拆分
            money_info['salary'] = money_info['salary'].str.split('-')

            money_info_low = money_info['salary'].str[0].str.split('K').str[0]
            # 格式转换 to_numeric把 str转为 浮点型
            mininfo = pandas.to_numeric(money_info_low).min()
            # 最低平均薪资
            meanmininfo = pandas.to_numeric(money_info_low).mean()


            # 最高薪资
            money_info_height = money_info['salary'].str[-1].str.split('K').str[0]
            maxinfo = pandas.to_numeric(money_info_height).max()
            # 最高平均薪资
            meanmaxinfo = pandas.to_numeric(money_info_height).mean()
            meaninfo = sum((meanmininfo, meanmaxinfo)) / 2

            # {'montypython': [2.0, 20.0, 10.58]}
            money_dict['name'] = name
            money_dict['money'] = [mininfo, maxinfo, numpy.around(meaninfo, decimals=2)]
            money_dict['posNum'] = posnum

            return money_dict

        #各个岗位的招聘数量,薪资

        dict_positionNum = {}
        money_list = []

        #值相等的情况
        # res_kaifa = res.loc[res['jobName'] == 'Python']



        #python 数量
        sel_python = res[res['jobName'].str.contains(r'.*?ython.*?')]
        posnum = sel_python['jobName'].count()   #岗位数量
        money_dict = dealmoney(sel_python, 'python', posnum)
        money_list.append(money_dict)
        # print(money_list)

        #运维数量
        sel_operation = res[res['jobName'].str.contains(r'.*?运维.*?')]
        posnum = sel_operation['jobName'].count()

        money_dict = dealmoney(sel_operation, '运维', posnum)
        money_list.append(money_dict)
        # print(money_list)

        #测试数量
        sel_test = res[res['jobName'].str.contains(r'.*?测试.*?')]
        posnum = sel_test['jobName'].count()

        money_dict = dealmoney(sel_test, '测试', posnum)
        money_list.append(money_dict)


        #人工智能数量
        sel_ai = res[res['jobName'].str.contains(r'.*?人工智能.*?')]
        posnum = sel_ai['jobName'].count()

        money_dict = dealmoney(sel_ai, '人工智能', posnum)
        money_list.append(money_dict)

        #大数据
        sel_bigdata = res[res['jobName'].str.contains(r'.*?大数据.*?')]
        posnum = sel_bigdata['jobName'].count()

        money_dict = dealmoney(sel_bigdata, '大数据', posnum)
        money_list.append(money_dict)

        #产品
        sel_product = res[res['jobName'].str.contains(r'.*?产品.*?')]
        posnum = sel_product['jobName'].count()

        money_dict = dealmoney(sel_product, '产品', posnum)
        money_list.append(money_dict)

        #java
        sel_java = res[res['jobName'].str.contains(r'.*?java.*?')]
        posnum = sel_java['jobName'].count()

        money_dict = dealmoney(sel_java, 'java', posnum)
        money_list.append(money_dict)

        #前端
        sel_front = res[res['jobName'].str.contains(r'.*?前端.*?')]
        posnum = sel_front['jobName'].count()

        money_dict = dealmoney(sel_front, '前端', posnum)
        money_list.append(money_dict)

        #数据分析
        sel_dataAnalyze = res[res['jobName'].str.contains(r'.*?数据分析.*?')]
        posnum = sel_dataAnalyze['jobName'].count()

        money_dict = dealmoney(sel_dataAnalyze, '数据分析', posnum)
        money_list.append(money_dict)

        # 爬虫
        sel_spider = res[res['jobName'].str.contains(r'.*?爬虫.*?')]
        posnum = sel_spider['jobName'].count()

        money_dict = dealmoney(sel_spider, '爬虫', posnum)
        money_list.append(money_dict)

        #算法
        sel_algorithms = res[res['jobName'].str.contains(r'.*?算法.*?')]
        posnum = sel_algorithms['jobName'].count()

        money_dict = dealmoney(sel_algorithms, '算法', posnum)
        money_list.append(money_dict)

        # 全栈
        sel_fulltree = res[res['jobName'].str.contains(r'.*?全栈.*?')]
        posnum = sel_fulltree['jobName'].count()

        money_dict = dealmoney(sel_fulltree, '全栈', posnum)
        money_list.append(money_dict)


        # print(res['eduLevel'])

        #分析学历
        res['eduLevel'] = res['eduLevel'].str.split(',').str[-1].str.split('\'').str[-2]
        # res[['salary']].groupby(['businessArea'], as_index=False).count()
        eduNum = res.groupby(['eduLevel']).count()['businessArea']

        # dict_res_area = res_area.set_index('businessArea').T.to_dict('int')
        #转换为字典形式

        dict_eduNum = eduNum.to_dict()
        list_eduNum = []
        for edu in dict_eduNum:
            #[{'edu': '不限', 'num': 22}, {'edu': '中专', 'num': 3},。。。
            list_eduNum.append({'edu': edu, 'num': dict_eduNum[edu]}) #转换为列表字典形式

        #留言板消息时间排序返回前端
        message = Contact.objects.all().order_by('-con_time')


        # con_name = models.CharField(verbose_name='姓名', max_length=30)
        # con_email = models.EmailField(verbose_name='邮箱')
        # con_number = models.CharField(verbose_name='手机号码', max_length=30)
        # con_message = models.TextField(verbose_name='留言信息')
        # con_time = models.DateTimeField(verbose_name='留言时间')

        return render(request, 'analyze.html', locals())

def Message(request):
    mesid = request.GET.get('mesid')
    message = Contact.objects.filter(id=mesid).first()
    return render(request, 'message.html', locals())

def Contactme(request):
    '''联系我'''
    if request.method == 'POST':
        print('收到据')
        yname = request.POST.get('YName')
        yemail = request.POST.get('YEmail')
        pnumber = request.POST.get('PNumber')
        message = request.POST.get('Message')
        con_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        con = Contact()
        con.con_name = yname
        con.con_email = yemail
        con.con_number = pnumber
        con.con_message = message
        con.con_time = con_time
        con.save()  #保存入数据库
        print('保存成功')
        return redirect('/job')
    else:
        print('未收到数据')
        return render(request, 'contact.html')
