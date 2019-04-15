# Generated by Django 2.1.7 on 2019-04-02 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0006_auto_20190313_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='edu',
            field=models.CharField(default='本科', max_length=20, verbose_name='学历'),
        ),
        migrations.AddField(
            model_name='user',
            name='honortitle',
            field=models.CharField(default='无', max_length=100, verbose_name='荣誉'),
        ),
        migrations.AddField(
            model_name='user',
            name='major',
            field=models.CharField(default='略', max_length=50, verbose_name='专业'),
        ),
        migrations.AddField(
            model_name='user',
            name='university',
            field=models.CharField(default='略', max_length=200, verbose_name='毕业院校'),
        ),
    ]
