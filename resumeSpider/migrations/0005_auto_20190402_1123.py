# Generated by Django 2.1.7 on 2019-04-02 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumeSpider', '0004_auto_20190319_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posbrief',
            name='businessArea',
            field=models.CharField(default='无', max_length=100, verbose_name='公司位置'),
        ),
    ]
