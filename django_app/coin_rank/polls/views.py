from django.http import HttpResponse
from django.shortcuts import render
from .models import Coin,TimeStamp,Historical,Rank,Price_Change
from .tables import BootstrapTable
from django_tables2 import RequestConfig
from .parse_coinmarket_cap import  get_all_coins,get_historical_data_for_url

def index(request):
    table = BootstrapTable(Coin.objects.all())
    RequestConfig(request, paginate=False).configure(table)
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

    testing = 0

    for coin in coin_to_url:
        url = coin_to_url[coin]
        if not Coin.objects.filter(coin_name=coin).exists():
            c = Coin(coin_name=coin,sector='',tech='',star=0,investment_memo='')
            c.save()
        get_historical_data_for_url(url,Coin.objects.get(coin_name=coin).get_id())
        if testing >= 2:
            break
        testing += 1

    all_coins = Coin.objects.all()
    all_timestamps = TimeStamp.objects.all()
    #
    # #calculate rank
    for timestamp in all_timestamps:
        coin_market_cap_ranking = dict()
        coin_obj_name_dict = dict()
        for coin in all_coins:
            coin_obj_name_dict[coin.coin_name] = coin
            try:
                h = Historical.objects.get(daily_timestamp=timestamp, coin_id=coin)
                coin_market_cap_ranking[coin.coin_name] =h.circulating_cap
            except:
                continue
        sorted_market_cap_ranking = sorted(coin_market_cap_ranking.items(), key=lambda kv: kv[1], reverse=True)
        rank = 1
        for (coin,market_cap) in sorted_market_cap_ranking:
            r = Rank(coin_id=coin_obj_name_dict[coin],daily_timestamp=timestamp,rank=rank)
            r.save()
            rank += 1

    #calculate price change
    for coin in all_coins:
        historicals = Historical.objects.all().filter(coin_id=coin).order_by('-daily_timestamp')
        for x in range(1,len(historicals)):
            historical = historicals[x]
            previous_price = historicals[x-1].average_price
            current_price = historical.average_price
            price_change_percantage = ((current_price - previous_price) / previous_price)
            p = Price_Change(coin_id=coin,daily_timestamp=historical.daily_timestamp,price_change=price_change_percantage)
            p.save()

    return index(request)