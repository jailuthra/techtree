# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-02 22:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
            ],
        ),
    ]
