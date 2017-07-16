from django import template
from datetime import date, timedelta

register = template.Library()
@register.filter(name='return_item')

def return_item(all_games, game):
    try:
        return all_games[game]
    except:
        return None
