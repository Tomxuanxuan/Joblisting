# Generated by Django 2.1.7 on 2019-03-12 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0003_honor_projects_skill_workexperience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='pro_brief',
            field=models.TextField(verbose_name='项目介绍'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='pro_environment',
            field=models.CharField(max_length=100, verbose_name='开发环境'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='pro_photo',
            field=models.ImageField(default='', upload_to='static/images/resume', verbose_name='图片'),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(default='', upload_to='static/images/resume', verbose_name='照片'),
        ),
        migrations.AlterField(
            model_name='workexperience',
            name='responsibility',
            field=models.TextField(verbose_name='职责'),
        ),
    ]
