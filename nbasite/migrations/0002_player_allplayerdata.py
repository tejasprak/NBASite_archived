# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-12 05:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nbasite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='allplayerdata',
            field=models.CharField(default='none', max_length=5),
            preserve_default=False,
        ),
    ]
