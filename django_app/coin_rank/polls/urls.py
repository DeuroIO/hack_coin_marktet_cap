from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    url(r'^coin/$', views.detail, name='Coin'),
    url(r'^slide_to', views.index, name='Slide'),
    url(r'sync_up', views.sync_up,name='Sync'),
    url(r'^save_memo/$', views.save_investment_memo, name='Memo'),
    url(r'^detail_rank/$',views.detail_rank_for_coin,name='Detail'),
]