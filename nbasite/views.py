# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
import pandas
import nba_py
from nba_py.constants import CURRENT_SEASON
from nba_py import constants
from nba_py import player
from nba_py import game
import json
import pprint
from nbasite.models import Player
from nbasite.forms import Name
from nbasite.models import Page
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_exempt
from django.template import *
from django import template
import re
import datetime
import wikipedia
from wikiapi import WikiApi



def find_scores_for_date(date):
    now = datetime.datetime.now()
    print now.year, now.month, now.day, now.hour, now.minute, now.second
    scoreboard = nba_py.Scoreboard(now.month, now.day, now.year)
    line_score_list = scoreboard.line_score()
    #print line_score_list
    number_of_games = (len(line_score_list))/2
    #print str(number_of_games) + " games on this day"
    i = 0
    games = []
    while(i != number_of_games):
        game_id = scoreboard.json['resultSets'][0]['rowSet'][i][2]
        i = i+1
        #print game_id
        games.append(game_id)
        #print games
    all_games = []
    z = 0
    for game in games:
        box = nba_py.game.BoxscoreSummary(str(game))
        box = box.line_score()
        box = box.values.tolist()
        hometeam = box[0][5]
        awayteam = box[1][5]
        hometeamscore = box[0][22]
        awayteamscore =  box[1][22]
        game_string = awayteam + " " + str(awayteamscore) + " " + hometeam + " " + str(hometeamscore)
        all_games.append(game_string)
        #['resultSets'][0]['rowSet'][0]
        z=z+1
    return all_games

def getInfoforPlayer(firstName, lastName):
    playerstats = {}
    playeri3d = nba_py.player.get_player(firstName, lastName, season='2016-17', only_current=0, just_id=True)
    stats = nba_py.player.PlayerSummary(playeri3d)
    #print stats
    headers = nba_py.player.PlayerSummary(playeri3d).json['resultSets'][0]['headers']
    #print headers
    i = 0
    for x in headers:
        playerstats[x] = stats.json['resultSets'][0]['rowSet'][0][i]
        i = i+1
    #print playerstats
    return playerstats

#class nameView(FormView):
#        template_name = 'index.html'
##        success_url = '/index/'
#        def form_valid(self, form):
#            # This method is called when valid form data has been POSTed.
#            # It should return an HttpResponse.
#            form.getPPG()
#            return super(nameView, self).form_valid(form)
def index(request):
    sentence = "Welcome to NBASite"
    #player_list = Player.PlayerCareerStats
    #player_list = eval(player_list)
    #player_list = Player.objects.all()
    #player_list = list(player_list)
    #for player in player_list

    player_list  = Player.objects.all()
    player_list = list(player_list)
    stat_list = Player.objects.all().values_list('ppg_percareer', flat=True)
    stat_list = [ float(x) for x in stat_list ]
    top_ppg_list = sorted(zip(stat_list, player_list), reverse=True)[:25]
    ppg_list_sentences = []
    i = 0
    for stat, player in top_ppg_list:
        ppg_list_sentences.append(str(player) + " : " + str(stat))
        i = i+1
    player_name = ''


    all_games = find_scores_for_date("5")


    context = RequestContext(request)
    context_dict = {'playername': player_name, 'playerstatsentence': sentence, 'players': ppg_list_sentences, 'all_games': all_games}
    return render_to_response('nbasite/index.html', context_dict, context)
def about(request):
    return HttpResponse("We out here")
@csrf_exempt
def newPlayer(request):
    if request.method == "POST":
        form = Name(request.POST)
        if form.is_valid():
            player = form.save(commit=False)

            name = player.name
            firstName, lastName = name.split(' ')
            player_id = nba_py.player.get_player(first_name=firstName, last_name=lastName, season='1980-81', only_current=0, just_id=True)
            json2 = nba_py.player.PlayerCareer(player_id, per_mode='PerGame', league_id='00')
            json3 = json2.regular_season_career_totals()
            pointspergameaverage = json3['PTS']
            pointspergame = json3['PTS'].values.tolist()
            pointspergameaverage = str(pointspergame[0])
            player.ppg_percareer=pointspergameaverage

            playerstats = {}
            playeri3d = nba_py.player.get_player(firstName, lastName, season='2016-17', only_current=0, just_id=True)
            joe =  nba_py.player.PlayerCareer(playeri3d, per_mode='PerGame', league_id='00')
            joe = joe.regular_season_career_totals()
            headers = joe.columns.values
            stats = joe.values.tolist()[0]
            #print stats[0]
            i = 0
            for x in headers:
                #rint stats[i]
                playerstats[x] = stats[i]
                i = i+1
                #print playerstats
            playerstats['firstName'] = firstName
            playerstats['lastName'] = lastName
            playerstats_string = repr(playerstats)
            player.PlayerCareerStats = playerstats_string
            personalinfo_string = repr(getInfoforPlayer(firstName, lastName))
            player.personalInfo = personalinfo_string
            player.save()
            #eturn redirect('post_detail', pk=post.pk)
    else:
        form = Name()
    context = RequestContext(request)
    context_dict = {'form': Name}
    return render_to_response('nbasite/addPlayer.html', context_dict, context)

def player(request, player_name_url):
    # Request our context from the request passed to us.
    context = RequestContext(request)

    # Change underscores in the category name to spaces.
    # URLs don't handle spaces well, so we encode them as underscores.
    # We can then simply replace the underscores with spaces again to get the name.
    #player_name = player_name_url.replace(' ', ' ')
    player_name = ""
    capitalLetters = 0
    if sum(1 for c in player_name_url if c.isupper()) > 2:
        print 'this name wont work'
        print player_name_url
        player = Player.objects.get(combinedName=player_name_url)
        print 'this name will work'
        player_name = str(player.combinedName)
        #print player
        capitalLetters = 1
    else:
        player_name = re.sub(r"(\w)([A-Z])", r"\1 \2", player_name_url)

    #player_name = re.sub(r"(\w)([A-Z])", r"\1 \2", player_name)
    print "tag" + player_name
    #player_name = 'Kristaps Porzingis'
    # Create a context dictionary which we can pass to the template rendering engine.
    # We start by containing the name of the category passed by the user.
    context_dict = {'player_name': player_name}


    # Can we find a category with the given name?
    # If we can't, the .get) method raises a DoesNotExist exception.
    # So the .get() method returns one model instance or raises an exception.
    if capitalLetters == 0:
        player = Player.objects.get(name=player_name)
        player1 = eval(player.PlayerCareerStats)
        player2 = eval(player.personalInfo)
    else:
        player = Player.objects.get(combinedName=player_name)
        player1 = eval(player.PlayerCareerStats)
        player2 = eval(player.personalInfo)
    #print player
    # Retrieve all of the associated pages.
    # Note that filter returns >= 1 model instance.
    #pages = Page.objects.filter(player=player)
    # Adds our results list to the template context under name pages.
    pages = "lol"
    context_dict['pages'] = pages
    # We also add the category object from the database to the context dictionary.
    # We'll use this in the template to verify that the category exists.
    context_dict['player'] = player1
    context_dict['player1'] = player2
    image = ""
    firstName = ""
    lastName = ""
    if capitalLetters == 0:
        firstName, lastName = player_name.split(' ')
        image = "https://nba-players.herokuapp.com/players/" + lastName + "/" +firstName
        player = Player.objects.get(name=player_name)
        thething = eval(player.personalInfo)
        if int(thething['DRAFT_YEAR']) < 2003:
            firstName = player.firstName
            lastName = player.lastName
            realname = firstName + " " + lastName
            #wikipagesuggest = wikipedia.suggest('Barack Obama')
            wiki = WikiApi()
            results = wiki.find(realname)
            article = wiki.get_article(results[0])
            if str(article.image) != 'http:None':
                image = article.image

    else:
        player = Player.objects.get(combinedName=player_name)
        firstName = player.firstName
        lastName = player.lastName
        realname = firstName + " " + lastName
        #wikipagesuggest = wikipedia.suggest('Barack Obama')
        wiki = WikiApi()
        results = wiki.find(realname)
        article = wiki.get_article(results[0])
        if str(article.image) != 'http:None':
            image = article.image

    context_dict['image'] = image

    # Go render the response and return it to the client.
    return render_to_response('nbasite/player.html', context_dict, context)
