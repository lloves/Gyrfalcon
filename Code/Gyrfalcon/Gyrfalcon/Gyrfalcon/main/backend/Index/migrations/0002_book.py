# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-25 07:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Index', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='名字')),
                ('authtor', models.CharField(default='', max_length=255, unique=True, verbose_name='作者')),
            ],
            options={
                'verbose_name': '书本',
                'db_table': 'index_book',
                'verbose_name_plural': '书本',
            },
        ),
    ]
