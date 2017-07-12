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
import json
import pprint
from nbasite.models import Player
from nbasite.forms import Name
from nbasite.models import Page
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_exempt

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
    player_list = Player.PlayerCareerStats
    #player_list = eval(player_list)
    category_list = Player.objects.order_by('-ppg_percareer')[:5]
    player_name = ''
    context = RequestContext(request)
    context_dict = {'playername': player_name, 'playerstatsentence': sentence, 'players': category_list}
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
    player_name = player_name_url.replace('_', ' ')

    # Create a context dictionary which we can pass to the template rendering engine.
    # We start by containing the name of the category passed by the user.
    context_dict = {'player_name': player_name}

    try:
        # Can we find a category with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        player = Player.objects.get(name=player_name)

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(player=player)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['player'] = player
    except Player.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render_to_response('nbasite/player.html', context_dict, context)
