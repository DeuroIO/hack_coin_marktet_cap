from django.http import HttpResponse
from django.shortcuts import render
from .models import Coin
from .tables import BootstrapTable
from django_tables2 import RequestConfig
from .parse_coinmarket_cap import  get_all_coins,get_historical_data_for_url

def index(request):
    table = BootstrapTable(Coin.objects.all())
    RequestConfig(request).configure(table)
    return render(request,'index.html', {'table': table})

def detail(request):
    in_name = request.GET.get('id', 'None')
    print(in_name)
    return render(request, 'detail.html')

def save_investment_memo(request):
    in_coin = request.POST.get('id', 'None')
    print(request)

def sync_up(request):
    coin_to_url = get_all_coins()
    for coin in coin_to_url:
        url = coin_to_url[coin]
        if not Coin.objects.filter(coin_name=coin).exists():
            c = Coin(coin_name=coin,sector='',tech='',star=0,investment_memo='')
            c.save()
        get_historical_data_for_url(url,Coin.objects.get(coin_name=coin).get_id())
    return index(request)