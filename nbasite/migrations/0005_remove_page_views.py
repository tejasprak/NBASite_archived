# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-12 09:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nbasite', '0004_auto_20170712_0616'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='views',
        ),
    ]