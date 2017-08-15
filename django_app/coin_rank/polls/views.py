from django.shortcuts import render
from .models import Coin,TimeStamp,Historical,Rank,Price_Change
from .parse_coinmarket_cap import  get_all_coins,get_historical_data_for_url
from .helper import beatifiy_a_number
import json
#!/usr/bin/env python
# -*- coding: utf-8 -*-

def index(request):
    slider_timestamps = TimeStamp.objects.all()
    id_to_timestamps_mapping = dict()
    for timestamp in slider_timestamps:
        id_to_timestamps_mapping[len(slider_timestamps) - timestamp.id + 1] = "{:%b, %d %Y}".format(timestamp.daily_timestamp)
    print(id_to_timestamps_mapping)
    if request.method == "POST":
        slider_value = request.POST.get('slider_value')
        slider_timestamp_id = len(slider_timestamps) - int(slider_value) + 1
        timestamp = TimeStamp.objects.get(id=slider_timestamp_id)
        slider_time_stamp = len(slider_timestamps) - timestamp.id + 1
    else:
        slider_time_stamp = len(slider_timestamps)
        timestamp = TimeStamp.objects.latest('daily_timestamp')
    coins = Coin.objects.all()
    if len(coins) == 0:
        return render(request,'index.html',{'coins':[]})

    bitcoin = Coin.objects.get(coin_name='Bitcoin')
    bitcoin_price = Historical.objects.get(coin_id=bitcoin,daily_timestamp=timestamp).average_price
    altered_coins = []
    for coin in coins:
        try:
            h = Historical.objects.get(coin_id=coin, daily_timestamp=timestamp)
            coin.average_price = "${0:.3f}".format(h.average_price)
            coin.volume = beatifiy_a_number(h.volume)
            coin.total_cap = "$" + str(beatifiy_a_number(h.total_cap))
            coin.circulating_cap = "$" + str(beatifiy_a_number(h.circulating_cap))
            coin.circulating_cap_bitcoin = "฿" + str(beatifiy_a_number(round(h.circulating_cap / bitcoin_price, 2)))
            r = Rank.objects.get(coin_id=coin, daily_timestamp=timestamp)
            coin.rank = r.rank
            p = Price_Change.objects.get(coin_id=coin, daily_timestamp=timestamp)
            coin.price_change = round(p.price_change, 2)
            altered_coins.append(coin)
        except:
            continue
    coins = sorted(altered_coins, key=lambda x: x.rank)

    return render(request,'index.html',{'coins':coins,"current_timestamp":slider_time_stamp,"max_timestamp":len(slider_timestamps),"id_to_timestamps_mapping":json.dumps(id_to_timestamps_mapping)})

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
        get_historical_data_for_url(url,Coin.objects.get(coin_name=coin))

    all_coins = Coin.objects.all()
    all_timestamps = TimeStamp.objects.all()
    # #
    # # #calculate rank
    for timestamp in all_timestamps:
        coin_market_cap_ranking = dict()
        for coin in all_coins:
            try:
                h = Historical.objects.get(daily_timestamp=timestamp, coin_id=coin)
                coin_market_cap_ranking[coin] =h.circulating_cap
            except:
                continue
        sorted_market_cap_ranking = sorted(coin_market_cap_ranking.items(), key=lambda kv: kv[1], reverse=True)
        rank = 1
        for (coin,market_cap) in sorted_market_cap_ranking:
            if not Rank.objects.filter(coin_id=coin).filter(daily_timestamp=timestamp).exists():
                r = Rank(coin_id=coin,daily_timestamp=timestamp,rank=rank)
                r.save()
            rank += 1

    # #calculate price change
    for coin in all_coins:
        historicals = Historical.objects.all().filter(coin_id=coin).order_by('-daily_timestamp')
        for x in range(1,len(historicals)):
            if not Price_Change.objects.filter(coin_id=coin).filter(daily_timestamp=timestamp).exists():
                historical = historicals[x]
                previous_price = historicals[x-1].average_price
                current_price = historical.average_price
                price_change_percantage = ((current_price - previous_price) / previous_price)
                p = Price_Change(coin_id=coin,daily_timestamp=historical.daily_timestamp,price_change=price_change_percantage)
                p.save()
    return index(request)