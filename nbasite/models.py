# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import pandas
import nba_py
from nba_py.constants import CURRENT_SEASON
from nba_py import constants
from nba_py import player
import json
import pprint

# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=128, unique=True)
    ppg_percareer = models.CharField(max_length=5, unique=False)
    personalInfo = models.CharField(max_length=2048, unique=False)
    PlayerCareerStats = models.CharField(max_length=2048, unique=False)
    def __unicode__(self):
        return self.name

class Page(models.Model):
    player = models.ForeignKey(Player)
    title = models.CharField(max_length=128)
    url = models.URLField()

    def __unicode__(self):
        return self.title
