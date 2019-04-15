from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

SEX = (
    (0, '女'),
    (1, '男'),
)

class User(AbstractUser):   #继承这个auth_user表
    '''用户信息表'''
    name = models.CharField(verbose_name='姓名', max_length=30)
    email = models.EmailField(verbose_name='邮箱地址')
    sex = models.BooleanField(verbose_name='性别', default=1, choices=SEX)
    phone = models.CharField(verbose_name='电话号码', max_length=11, null=True, blank=True)
    birth_time = models.DateField(verbose_name='出生年月', null=True)
    photo = models.ImageField(verbose_name='照片', upload_to='static/images/resume', default='')
    address = models.CharField(verbose_name='住址', max_length=50, null=True)
    aboutme = models.CharField(verbose_name='个人简介', max_length=300, null=True)
    university = models.CharField(verbose_name='毕业院校', max_length=200, default='略')
    major = models.CharField(verbose_name='专业', max_length=50, default='略')
    edu = models.CharField(verbose_name='学历', max_length=20, default='本科')
    honortitle = models.CharField(verbose_name='荣誉', max_length=100, default='无')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Users'
        verbose_name = '用户信息表'
        verbose_name_plural = verbose_name

class Skill(models.Model):
    '''专业技能表'''
    skillinfo = models.TextField(verbose_name='专业技能')

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.skillinfo

    class Meta:
        db_table = 'Skill'
        verbose_name = '专业技能表'
        verbose_name_plural = verbose_name

class WorkExperience(models.Model):
    '''工作经历表'''
    id = models.IntegerField(primary_key=True)
    worktime = models.CharField(verbose_name='工作时间', max_length=30)
    company = models.CharField(verbose_name='公司', max_length=30)
    position = models.CharField(verbose_name='职位', max_length=30)
    responsibility = models.TextField(verbose_name='职责')

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.company

    class Meta:
        db_table = 'WorkExperience'
        verbose_name = '工作经历表'
        verbose_name_plural = verbose_name


class Projects(models.Model):
    '''项目经验表'''
    pro_name = models.CharField(verbose_name='项目名称', max_length=30)
    pro_environment = models.CharField(verbose_name='开发环境', max_length=100)
    pro_brief = models.TextField(verbose_name='项目介绍')
    pro_photo = models.ImageField(verbose_name='图片', upload_to='static/images/resume', default='')
    pro_responsibility = models.CharField(verbose_name='项目职责', max_length=200)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.pro_name

    class Meta:
        db_table = 'Projects'
        verbose_name = '项目经验表'
        verbose_name_plural = verbose_name

class Honor(models.Model):
    '''荣誉证书'''
    hon_name = models.CharField(verbose_name='证书名称', max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.hon_name

    class Meta:
        db_table = 'Honor'
        verbose_name = '荣誉证书表'
        verbose_name_plural = verbose_name

class Contact(models.Model):
    '''留言表'''
    con_name = models.CharField(verbose_name='姓名', max_length=30)
    con_email = models.EmailField(verbose_name='邮箱')
    con_number = models.CharField(verbose_name='手机号码', max_length=30)
    con_message = models.TextField(verbose_name='留言信息')
    con_time = models.DateTimeField(verbose_name='留言时间')

    def __str__(self):
        return self.con_name
    class Meta:
        db_table = 'Contact'
        verbose_name = '留言表'
        verbose_name_plural = verbose_name

