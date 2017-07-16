from django import forms
from nbasite.models import Player

#class Name(forms.Form):
#    firstName = forms.CharField()
#    lastName = forms.CharField()
#    def getPPG(self):
#        player_id = nba_py.player.get_player(first_name=firstName, last_name=lastName, season='1961-62', only_current=0, just_id=True)
#        pointspergameaverage = json3['PTS']
#        pointspergame = json3['PTS'].values.tolist()
#        pointspergameaverage = str(pointspergame[0])
#        return HttpResponse(pointspergameaverage)

class Name(forms.ModelForm):

    class Meta:
        model = Player
        ppg_percareer = "35"
        fields = ('name',)
class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
    end_date = forms.DateField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                })) 
