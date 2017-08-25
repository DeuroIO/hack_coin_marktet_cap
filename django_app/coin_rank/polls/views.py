from django.shortcuts import render
from .models import Coin,TimeStamp,Historical,Rank,Price_Change
from .parse_coinmarket_cap import  get_all_coins,get_historical_data_for_url
from .helper import beatifiy_a_number,millify
import datetime
import numpy
from django.http import JsonResponse
import json
from threading import Timer
#!/usr/bin/env python
# -*- coding: utf-8 -*-

def index(request):
    slider_timestamps = TimeStamp.objects.all()
    if request.method == "POST":
        slider_value = request.POST.get('slider_value')
        slider_time_stamp = int(slider_value)
        timestamp = TimeStamp.objects.get(id=slider_time_stamp)
    else:
        slider_time_stamp = len(slider_timestamps)
        if len(slider_timestamps) == 0:
            return render(request,'index.html',{'coins':[]})
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
            coin.volume = "$" + str(millify(h.volume))
            coin.total_cap = "$" + str(millify(h.total_cap))
            coin.circulating_cap = "$" + str(millify(h.circulating_cap))
            coin.circulating_cap_bitcoin = "B " + str(millify(round(h.circulating_cap / bitcoin_price, 2)))
            print(coin)
            try:
                r = Rank.objects.get(coin_id=coin, daily_timestamp=timestamp)
                coin.rank = r.rank
                print(coin.rank)
            except:
                pass
            try:
                p = Price_Change.objects.get(coin_id=coin, daily_timestamp=timestamp)
                print(p)
                coin.price_change = round(p.price_change, 2) * 100
                print(coin.price_change)
            except:
                print("dones't have price change for {} at {} ".format(coin,timestamp))
                pass
                
            #print(coin)
            #print(coin.price_change)
            altered_coins.append(coin)
        except:
            continue
    #Sanity check to remove coin if it doesn't have rank
    altered_coins = [s for s in altered_coins if hasattr(s, 'rank')]
    coins = sorted(altered_coins, key=lambda x: x.rank)

    timestamp_s = timestamp.daily_timestamp.strftime('%Y-%b-%d')
    return render(request,'index.html',{'coins':coins,"current_timestamp":slider_time_stamp,"max_timestamp":len(slider_timestamps),'timestamp_s':timestamp_s})

def detail(request):
    id = request.GET.get('id', 'None')
    coin_name = Coin.objects.get(id=id).coin_name
    return render(request, 'detail.html',{'token_title':coin_name})

def detail_rank_for_coin(request):
    id = request.GET.get('id')
    array = []
    coin = Coin.objects.get(id=id)
    timestamps = TimeStamp.objects.all().order_by('daily_timestamp')
    for timestamp in timestamps:
        try:
            r = Rank.objects.get(coin_id=coin,daily_timestamp=timestamp)
            array.append([timestamp.daily_timestamp, r.rank])
        except:
            continue
    return JsonResponse(array,safe=False)

def detail_cap_for_coin(request):
    id = request.GET.get('id')
    array = []
    coin = Coin.objects.get(id=id)
    timestamps = TimeStamp.objects.all().order_by('daily_timestamp')
    for timestamp in timestamps:
        try:
            h = Historical.objects.get(coin_id=coin, daily_timestamp=timestamp)
            array.append([timestamp.daily_timestamp, h.circulating_cap])
        except:
            continue
    return JsonResponse(array, safe=False)

def save_investment_memo(request):
    in_coin = request.POST.get('id', 'None')
    print(request)

def sync_up(request=None):
    coin_to_url = get_all_coins()

    #For adding sorted timestamps
    coin_timestamp_historical_dict = dict()
    timestamps_set = set()
    #testing = 0
    for coin in coin_to_url:
        url = coin_to_url[coin]
        small_time_dict,small_timestamp_set = get_historical_data_for_url(url)
        timestamps_set = timestamps_set.union(small_timestamp_set)
        coin_timestamp_historical_dict[coin] = small_time_dict
        #if testing > 1:
        #    break
        #testing += 1

    timestamps_set_list = list(timestamps_set)
    timestamps_set_list.sort()
    for m_timestamp in timestamps_set_list:
        if not TimeStamp.objects.all().filter(daily_timestamp=m_timestamp).exists():
            t = TimeStamp(daily_timestamp=m_timestamp)
            t.save()

    #For adding coins & historicals
    for coin in coin_timestamp_historical_dict:
        if not Coin.objects.filter(coin_name=coin).exists():
            c = Coin(coin_name=coin,sector='',tech='',star=0,investment_memo='')
            c.save()
        coin_obj = Coin.objects.get(coin_name=coin)
        for timestamp in timestamps_set:
            t = TimeStamp.objects.get(daily_timestamp=timestamp)
            if timestamp in coin_timestamp_historical_dict[coin]:
                h_small_dict = coin_timestamp_historical_dict[coin][timestamp]
                if not Historical.objects.all().filter(coin_id=coin_obj).filter(daily_timestamp=t).exists():
                    h = Historical(coin_id=coin_obj, daily_timestamp=t, average_price=h_small_dict["average_price"],
                    volume=h_small_dict['volume'], circulating_cap=h_small_dict['circulating_cap'],
                    total_cap=h_small_dict['total_cap'])
                    h.save()
                else:
                    h = Historical.objects.get(coin_id=coin_obj,daily_timestamp=t)
                    h.total_cap = h_small_dict['total_cap']
                    h.save

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
        for x in range(1,len(all_timestamps)):
            timestamp = all_timestamps[x]
            prev_timestamp = all_timestamps[x-1]
            print("{} {}:{}".format(coin,timestamp,Price_Change.objects.filter(coin_id=coin).filter(daily_timestamp=timestamp).exists()))
            if not Price_Change.objects.filter(coin_id=coin).filter(daily_timestamp=timestamp).exists():
                try:
                    historical = Historical.objects.get(coin_id=coin,daily_timestamp=timestamp)
                    previous_hist = Historical.objects.get(coin_id=coin,daily_timestamp=prev_timestamp)
                    current_price = historical.average_price
                    previous_price = previous_hist.average_price
                    price_change_percantage = ((current_price - previous_price) / previous_price)
                    p = Price_Change(coin_id=coin,daily_timestamp=historical.daily_timestamp,price_change=price_change_percantage)
                    p.save()
                except:
                    continue
    Timer(interval, sync_up).start()
    return index(request)

interval = 3600 * 20   #interval (4hours)
