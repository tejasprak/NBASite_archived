from django import forms
from nbasite.models import Player
from functools import partial
from django.contrib.admin import widgets

#class Name(forms.Form):
#    firstName = forms.CharField()
#    lastName = forms.CharField()
#    def getPPG(self):
#        player_id = nba_py.player.get_player(first_name=firstName, last_name=lastName, season='1961-62', only_current=0, just_id=True)
#        pointspergameaverage = json3['PTS']
#        pointspergame = json3['PTS'].values.tolist()
#        pointspergameaverage = str(pointspergame[0])
#        return HttpResponse(pointspergameaverage)
TEAMS = (
    ('ATL', 'Atlanta Hawks'),
    ('BKN', 'Brooklyn Nets'),
    ('BOS', 'Boston Celtics'),
    ('CHA', 'Charlotte Hornets'),
    ('CHI', 'Chicago Bulls'),
    ('CLE', 'Cleveland Cavaliers'),
    ('DAL', 'Dallas Mavericks'),
    ('DEN', 'Denver Nuggets'),
    ('DET', 'Detroit Pistons'),
    ('GSW', 'Golden State Warriors'),
    ('HOU', 'Houston Rockets'),
    ('IND', 'Indiana Pacers'),
    ('LAC', 'Los Angeles Clippers'),
    ('LAL', 'Los Angeles Lakers'),
    ('MEM', 'Memphis Grizzlies'),
    ('MIA', 'Miami Heat'),
    ('MIL', 'Milwaukee Bucks'),
    ('MIN', 'Minnesota Timberwolves'),
    ('NOP', 'New Orleans Pelicans'),
    ('NYK', 'New York Knicks'),
    ('OKC', 'Oklahoma City Thunder'),
    ('ORL', 'Orlando Magic'),
    ('PHI', 'Philadelphia 76ers'),
    ('PHX', 'Phoenix Suns'),
    ('POR', 'Portland Trail Blazers'),
    ('SAC', 'Sacramento Kings'),
    ('SAS', 'San Antonio Spurs'),
    ('UTA', 'Utah Jazz'),
    ('WAS', 'Washington Wizards'),
)

class Name(forms.ModelForm):

    class Meta:
        model = Player
        ppg_percareer = "35"
        fields = ('name',)
DateInput = partial(forms.DateInput, {'class': 'datepicker'})
class GameForm(forms.Form):
    date = forms.DateField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
    end_date = forms.DateField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
