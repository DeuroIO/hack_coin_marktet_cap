from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    url(r'^coin/$', views.detail, name='Coin'),
    url(r'sync_up', views.sync_up,name='Sync'),
    url(r'^save_memo/$', views.save_investment_memo, name='Memo'),
]