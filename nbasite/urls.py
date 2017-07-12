from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about', views.about, name = 'about'),
    url(r'^new/$', views.newPlayer, name='newPlayer'),
    url(r'^player/(?P<player_name_url>\w+)/$', views.player, name='player'),
]
