# Generated by Django 2.1.7 on 2019-03-16 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Positions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pos_title', models.CharField(max_length=30, verbose_name='岗位')),
                ('pos_salary', models.CharField(max_length=30, verbose_name='薪资')),
                ('pos_company', models.CharField(max_length=30, verbose_name='公司名称')),
                ('pos_address', models.CharField(max_length=100, verbose_name='公司地址')),
                ('pos_company_brief', models.TextField(verbose_name='公司简介')),
                ('pos_content', models.TextField(verbose_name='岗位描述')),
                ('pos_bright', models.CharField(max_length=100, verbose_name='岗位亮点')),
            ],
            options={
                'verbose_name': '职位表',
                'verbose_name_plural': '职位表',
                'db_table': 'Positions',
            },
        ),
    ]
