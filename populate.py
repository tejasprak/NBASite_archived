# List of imported season: 2016-17, 1961-62, 1984-85


#more efficient population system

import os

import pandas
import nba_py
from nba_py.constants import CURRENT_SEASON
from nba_py import constants
from nba_py import player
from nba_py import league
from nba_py import game
from nba_py import team
import json
import pprint
import django
import requests

def statleader(season, stat2):
    playerstats = {}
    seasonbegin, seasonend = season.split('-')
    seasonbegin = int(seasonbegin)
    stat = nba_py.league.Leaders('00', 'PerGame', stat2, season, 'Regular Season')
    data = stat.json['resultSet']['headers']
    i = 0
    for x in data:
        playerstats[x] = stat.json['resultSet']['rowSet'][0][i]
        i = i+1
    playerstats[u'Name'] = playerstats['PLAYER']
    return playerstats
def getInfoforPlayerID(playerid):
    playerstats = {}
    playeri3d = playerid
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
def getStatsforPlayer(firstName, lastName):
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
    return playerstats
def getStatsforPlayerID(playerid):
    playerstats = {}
    playeri3d = playerid
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
    #print playerstats
    #playerstats['firstName'] = firstName
    #playerstats['lastName'] = lastName
    return playerstats
#joe = statleader('1961-62', 'PTS')
#print joe['Name']
#print joe['PTS']
#firstname = raw_input('Enter first name ')
#lastname = raw_input('Enter last name ')
#career_stat = raw_input('Career average stat? ')
#print getStatsforPlayer(firstname, lastname)[career_stat]
#joe = getInfoforPlayer("James", "Harden")
#print type(joe)


#stat2 = stat.headline_stats()
#print stat2



#repr





def populate(year):
    year = year * 100000

    year = 20000000 + year + 1
    print year
    game_id = year
    game_end = 21501230
    while game_id != game_end:
        realgameid = "00" + str(game_id)
        print realgameid
        game = nba_py.game.Boxscore(str(realgameid), season='2016-2017', season_type='Regular Season')
        player_names =  game.player_stats()['PLAYER_NAME']
        #print hi
        #print type(player_names)
        playerlist = player_names.tolist()
        #print playerlist
        #print hi
        for player in playerlist:
            print player
            playernamename = str(player)
            firstName = ""
            lastName = ""
            if(len(playernamename.split()) == 2):
                firstName, lastName = player.split(' ')
            if(len(playernamename.split()) == 1):
                firstName = player
                lastName = None
                print "hi"
            if(len(playernamename.split()) > 2):
                #firstName, lastName, x = player.split(' ')
                break
            ppgcareer = getStatsforPlayer(firstName, lastName)['PTS']
            print "Hi"
            combinedName = firstName + str(lastName)
            playerinfo = repr(getInfoforPlayer(firstName, lastName))
            playerstats = repr(getStatsforPlayer(firstName, lastName))
            Player.objects.get_or_create(name=player,ppg_percareer=ppgcareer,personalInfo=playerinfo,PlayerCareerStats=playerstats, firstName = firstName, lastName = lastName, combinedName=combinedName)

        game_id = game_id + 1

def populate2():
    game_id = 29300001
    game_end = 29301230
    while game_id != game_end:
        realgameid = "00" + str(game_id)

        game = nba_py.game.Boxscore(realgameid, season='1993-94', season_type='Regular Season')
        player_names =  game.player_stats()['PLAYER_NAME']
        #print type(player_names)
        playerlist = player_names.tolist()
        #print playerlist
        for player in playerlist:
            print player
            playernamename = str(player)
            if(len(playernamename.split()) == 2):
                firstName, lastName = player.split(' ')
            if(len(playernamename.split()) == 1):
                firstName = player
                lastName = None
            if(len(playernamename.split()) > 2):
                #firstName, lastName, x = player.split(' ')
                break
            ppgcareer = getStatsforPlayer(firstName, lastName)['PTS']
            playerinfo = repr(getInfoforPlayer(firstName, lastName))
            playerstats = repr(getStatsforPlayer(firstName, lastName))
            Player.objects.get_or_create(name=player,ppg_percareer=ppgcareer,personalInfo=playerinfo,PlayerCareerStats=playerstats)

        game_id = game_id + 1
def population():
    #teams = json.load("teams.json")
    r = requests.get("https://raw.githubusercontent.com/bttmly/nba/master/data/teams.json")
    r = r.json()
    i = 0
    teams = []
    while i < 30:
        teams.append(r[i]['teamId'])
        i = i+1
    for team in teams:
        roster = nba_py.team.TeamCommonRoster(team, season='1984-85').roster()
        rosterlist = roster.values.tolist()
        #print len(rosterlist)
        f = 0
        while f < len(rosterlist):
            ids = roster.values.tolist()[f][12]
            #print ids
            name = roster.values.tolist()[f][3]
            print name
            #print name
            ppgcareer = getStatsforPlayerID(ids)['PTS']
            personal = repr(getInfoforPlayerID(ids))
            playerstats = repr(getStatsforPlayerID(ids))
            first =  getInfoforPlayerID(ids)['FIRST_NAME']
            last =  getInfoforPlayerID(ids)['LAST_NAME']
            combinedname = first + last
            #print combinedname
            Player.objects.get_or_create(name=name,ppg_percareer=ppgcareer,personalInfo=personal,PlayerCareerStats=playerstats,firstName=first,lastName=last,combinedName=combinedname)

            #first =
            f = f + 1
if __name__ == '__main__':
    print "Starting NBA player population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nba.settings')
    django.setup()
    from nbasite.models import Player
    population()
    #populate(61)
    #populate2()

#name = models.CharField(max_length=128, unique=True)

#ppg_percareer = models.CharField(max_length=5, unique=False)
#ersonalInfo = models.CharField(max_length=2048, unique=False)
##PlayerCareerStats = models.CharField(max_length=2048, unique=False)
#firstName = models.CharField(max_length=128, unique=False)
#lastName = models.CharField(max_length=128, unique=False)
#combinedName = models.CharField(max_length=128, unique=False)
