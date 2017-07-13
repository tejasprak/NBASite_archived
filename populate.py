import os

import pandas
import nba_py
from nba_py.constants import CURRENT_SEASON
from nba_py import constants
from nba_py import player
from nba_py import league
from nba_py import game
import json
import pprint
import django

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





def populate():
    game_id = 26100001
    game_end = 26101230
    while game_id != game_end:
        realgameid = "00" + str(game_id)

        game = nba_py.game.Boxscore(realgameid, season='1961-62', season_type='Regular Season')
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


if __name__ == '__main__':
    print "Starting NBA player population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nba.settings')
    django.setup()
    from nbasite.models import Player
    populate()
