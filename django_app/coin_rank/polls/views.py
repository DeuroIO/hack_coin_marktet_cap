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
        ico = 'None'
    else:
        slider_time_stamp = len(slider_timestamps)
        if len(slider_timestamps) == 0:
            return render(request,'index.html',{'coins':[]})
        timestamp = TimeStamp.objects.latest('daily_timestamp')

        # Check GET to see if use good_ico or bad_ico
        ico = request.GET.get('ico', 'None')
    coins = Coin.objects.all()
    if 'good' == ico:
        filtered_coins = []
        for coin in coins:
            coin_historicals = Historical.objects.filter(coin_id=coin).order_by('daily_timestamp')
            intail_ico_price = coin_historicals[0].average_price
            two_x_intail_ico_price = 2 * intail_ico_price
            last_index = min(31,len(coin_historicals))
            for h_index in range(1,last_index):
                if coin_historicals[h_index].average_price >= two_x_intail_ico_price:
                    filtered_coins.append(coin)
                    #current price is 2x than intail_ico_price.
                    #add it to the filtered_coins
                    #next coins
                    break
        coins = filtered_coins
    elif 'bad' == ico:
        filtered_coins = []
        for coin in coins:
            coin_historicals = Historical.objects.filter(coin_id=coin).order_by('daily_timestamp')
            intail_ico_price = coin_historicals[0].average_price
            one_point_five_intail_ico_price = 1.5 * intail_ico_price
            is_always_lower_than_one_point_five = True
            last_index = min(31,len(coin_historicals))
            for h_index in range(1, last_index):
                if coin_historicals[h_index].average_price > one_point_five_intail_ico_price:
                    #current price is greater than half_intail_ico_price
                    #it is not a bad coins
                    # next coins
                    is_always_lower_than_one_point_five = False
                    break
            if is_always_lower_than_one_point_five:
                filtered_coins.append(coin)
        coins = filtered_coins

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
            try:
                r = Rank.objects.get(coin_id=coin, daily_timestamp=timestamp)
                coin.rank = r.rank
            except:
                print("dones't have rank for {} at {}".format(coin,timestamp))
                pass
            try:
                p = Price_Change.objects.get(coin_id=coin, daily_timestamp=timestamp)
                coin.price_change = round(p.price_change, 2) * 100
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

    #fix img path
    for coin in coins:
        coin.image = coin.image.url[6:]
    #if ico parameters != None
    if ico != 'None':
      if ico == 'bad':
          ico_description = "Within the first month of its ICO, the average price of this coin is smaller than 1.5x of its ICO price"
      else:
          ico_description = "Within the first month of its ICO, the average price of this coin is 2x > than its ICO price"
      return render(request,'ico.html',{'coins':coins,"current_timestamp":slider_time_stamp,"max_timestamp":len(slider_timestamps),'timestamp_s':timestamp_s,'ico':ico,'ico_description':ico_description})
    else:
      return render(request,'index.html',{'coins':coins,"current_timestamp":slider_time_stamp,"max_timestamp":len(slider_timestamps),'timestamp_s':timestamp_s})

def good_ico(request):
    request.GET._mutable = True
    request.GET['ico'] = 'good'
    return index(request)

def bad_ico(request):
    request.GET._mutable = True
    request.GET['ico'] = 'bad'
    return index(request)

def detail(request):
    id = request.GET.get('id', 'None')
    coin_name = Coin.objects.get(id=id).coin_name

    slider_timestamps = TimeStamp.objects.all()
    if request.method == "POST":
        slider_value = request.POST.get('slider_value')
        slider_time_stamp = int(slider_value)
        timestamp = TimeStamp.objects.get(id=slider_time_stamp)
        ico = 'None'
    else:
        slider_time_stamp = len(slider_timestamps)
        timestamp = TimeStamp.objects.latest('daily_timestamp')
    print(slider_time_stamp)
    return render(request, 'detail.html',{'token_title':coin_name,"current_timestamp":slider_time_stamp,"max_timestamp":len(slider_timestamps)})

#pre-fetch rank information for all the coins
global_coin_rank_dict = dict()
global_coin_cap_dict = dict()

#helper function to populate global_coin_rank_dict
def populate_gobal_coin_rank_dict():
    global global_coin_rank_dict
    global_coin_rank_dict = dict()

    global global_coin_cap_dict
    global_coin_cap_dict = dict()

    coins = Coin.objects.all()
    timestamps = TimeStamp.objects.all().order_by('daily_timestamp')
    
    counter = 1
    for coin in coins:
        print("{} : {}".format(counter,coin))
        counter += 1
        rank_array = []
        cap_array = []
        for timestamp in timestamps:
            try:
                r = Rank.objects.get(coin_id=coin,daily_timestamp=timestamp)
                rank_array.append([timestamp.daily_timestamp, r.rank])
            except:
                pass
            try:
                h = Historical.objects.get(coin_id=coin, daily_timestamp=timestamp)
                cap_array.append([timestamp.daily_timestamp, h.circulating_cap])
            except:
                pass
        if counter == 5:
            break
        if len(rank_array) != 0:
            global_coin_rank_dict[coin.id] = rank_array
        if len(cap_array) != 0:
            global_coin_cap_dict[coin.id] = cap_array
        

def detail_rank_for_coin(request):
    id = int(request.GET.get('id'))
    if id in global_coin_rank_dict:
        array = global_coin_rank_dict[id]
        return JsonResponse(array,safe=False)
    else:
        return JsonResponse([],safe=False)

def detail_cap_for_coin(request):
    id = int(request.GET.get('id'))
    if id in global_coin_cap_dict:
        array = global_coin_cap_dict[id]
        return JsonResponse(array, safe=False)
    else:
        return JsonResponse([],safe=False)

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
        url,img_name = coin_to_url[coin]
        small_time_dict,small_timestamp_set = get_historical_data_for_url(url)
        timestamps_set = timestamps_set.union(small_timestamp_set)
        coin_timestamp_historical_dict[coin] = [small_time_dict,img_name]
        #if testing > 1:
        #   break
        #testing += 1

    timestamps_set_list = list(timestamps_set)
    timestamps_set_list.sort()
    for m_timestamp in timestamps_set_list:
        if not TimeStamp.objects.all().filter(daily_timestamp=m_timestamp).exists():
            t = TimeStamp(daily_timestamp=m_timestamp)
            t.save()

    #For adding coins & historicals
    for coin in coin_timestamp_historical_dict:
        small_time_dict, img_name = coin_timestamp_historical_dict[coin]
        if not Coin.objects.filter(coin_name=coin).exists():
            c = Coin(coin_name=coin,image=img_name,sector='',tech='',star=0,investment_memo='')
            c.save()
        coin_obj = Coin.objects.get(coin_name=coin)
        for timestamp in timestamps_set:
            t = TimeStamp.objects.get(daily_timestamp=timestamp)
            if timestamp in small_time_dict:
                h_small_dict = small_time_dict[timestamp]
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
#populate_gobal_coin_rank_dict()
