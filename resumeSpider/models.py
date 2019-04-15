from django.db import models

# Create your models here.

class Posbrief(models.Model):
    '''职位简介表'''
    businessArea = models.CharField(verbose_name='公司位置',max_length=100, default='无')
    createDate = models.DateTimeField(verbose_name='创建日期')
    jobName = models.CharField(verbose_name='岗位名称', max_length=100)
    positionURL = models.URLField(verbose_name='地址链接', primary_key=True)
    salary = models.CharField(verbose_name='薪资', max_length=30)
    updateDate = models.DateTimeField(verbose_name='更新时间')

    company = models.CharField(verbose_name='公司', max_length=500, default='')
    companyLogo = models.CharField(verbose_name='logo', max_length=150, default='')
    eduLevel = models.CharField(verbose_name='学历', max_length=50, default='')
    jobTag = models.CharField(verbose_name='工作福利', max_length=100, default='')
    jobType = models.CharField(verbose_name='工作类型', max_length=300, default='')

    def __str__(self):
        return self.jobName
    class Meta:
        db_table = 'Posbrief'
        verbose_name = '职位简介表'
        verbose_name_plural = verbose_name


class Positions(models.Model):
    '''职位表'''
    pos_url = models.OneToOneField(Posbrief, on_delete=models.CASCADE)
    pos_title = models.CharField(verbose_name='岗位', max_length=30)
    pos_salary = models.CharField(verbose_name='薪资', max_length=30)
    pos_company = models.CharField(verbose_name='公司名称', max_length=30)
    pos_address = models.CharField(verbose_name='公司地址', max_length=100)
    pos_company_brief = models.TextField(verbose_name='公司简介')
    pos_content = models.TextField(verbose_name='岗位描述')
    pos_bright = models.CharField(verbose_name='岗位亮点', max_length=100)


    def __str__(self):
        return self.pos_title
    class Meta:
        db_table = 'Positions'
        verbose_name = '职位表'
        verbose_name_plural = verbose_name
