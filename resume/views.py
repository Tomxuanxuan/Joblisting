from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .models import *
import json
import datetime

# Create your views here.
def index(request):
    '''主页'''
    user_id = request.session.get('user_id')
    if not user_id:
        user_id = 1
    myself = User.objects.filter(id=user_id).first()
    project = Projects.objects.filter(user_id=user_id).all()
    skills = Skill.objects.filter(user=user_id).all()
    return render(request, 'myindex.html', locals())

def workexperience(request):
    '''工作经历'''
    if request.method == 'GET':
        user_id = request.GET.get('user')
        if not user_id:
            user_id = 1

        work_exps = WorkExperience.objects.filter(user=user_id).order_by('worktime').all()
        list_workexp = []
        for work_exp in work_exps:
            data = {
                'id': work_exp.id,
                'worktime': work_exp.worktime,
                'company': work_exp.company,
                'position': work_exp.position,
                'responsibility': work_exp.responsibility
            }
            list_workexp.append(data)

        workjsStr = json.dumps(list_workexp)
        return HttpResponse(workjsStr)

def project(request):
    '''项目经验'''
    pass


def contactme(request):
    '''联系我'''
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
    return redirect('/job')



def login_views(request):
    '''登录'''
    if request.method == 'POST':
        uname = request.POST.get('username')
        upwd = request.POST.get('password')

        res = User.objects.filter(username=uname)
        if not res:
            return render(request, 'login.html', {'errMsg': '用户名不存在'})
        else:
            user = authenticate(username=uname, password=upwd)
            if user is not None and user.is_active:
                login(request, user)
                request.session['user_id'] = user.id    #保存信息进 session
                request.session['name'] = user.name
                return redirect('/job')
            else:
                return render(request, 'login.html', {'errMsg': '用户名或密码错误'})
    else:
        return render(request, 'login.html')

def logout_view(request):
    '''退出'''
    logout(request)
    return redirect('/job')
