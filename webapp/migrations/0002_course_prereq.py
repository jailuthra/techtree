# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-02 22:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='prereq',
            field=models.ManyToManyField(to='webapp.Course'),
        ),
    ]
