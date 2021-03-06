# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-03 15:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identify_number', models.CharField(max_length=18, unique=True)),
                ('full_name', models.CharField(max_length=64)),
                ('account_number', models.CharField(max_length=64)),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
