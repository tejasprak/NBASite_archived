# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-15 23:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('ppg_percareer', models.CharField(max_length=5)),
                ('personalInfo', models.CharField(max_length=2048)),
                ('PlayerCareerStats', models.CharField(max_length=2048)),
                ('firstName', models.CharField(max_length=128)),
                ('lastName', models.CharField(max_length=128)),
                ('combinedName', models.CharField(max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nbasite.Player'),
        ),
    ]
