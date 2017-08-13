import urllib
from bs4 import BeautifulSoup
import sys
from re import sub
from decimal import Decimal

if sys.version_info[0] == 3:
    from urllib.request import urlopen
else:
    # Not Python 3 - today, it is most likely to be Python 2
    # But note that this might need an update when Python 4
    # might be around one day
    from urllib import urlopen

def get_html_by_url(url):
    # Your code where you can use urlopen
    response = urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def get_decimal_from_currency_string(money):
    value = Decimal(sub(r'[^\d.]', '', money))
    return value

base_url = 'https://coinmarketcap.com'
soup = get_html_by_url(base_url)
arrs = soup.findAll('td',{'class':'no-wrap currency-name'})
coin_to_url = dict()
for arr in arrs:
    imgs = arr.findAll('img',{'class':'currency-logo'})
    name = imgs[0]['alt']

    link = base_url + arr.findAll('a')[0]['href'] + "#markets"
    coin_to_url[name] = link

minimum_requirement_for_volume = 100000.0
coin_markets_abs = dict()
coin_markets_per = dict()
coin_to_links = dict()
for coin in coin_to_url:
    link = coin_to_url[coin]
    coin_soup = get_html_by_url(link)
    standard_price = get_decimal_from_currency_string(coin_soup.findAll('span',{'class':'text-large','id':'quote_price'})[0].text)
    tbody = coin_soup.findAll('tbody')[0]
    trs = tbody.findAll('tr')
    print(coin)
    print(standard_price)
    lowerest_price_to_buy = standard_price
    highest_price_to_sell = standard_price
    lowerest_price_link = ''
    highest_price_link = ''
    for tr in trs:
        tds = tr.findAll('td')
        recently_exists = False
        volume = tr.findAll('span',{'class':'volume'})[0].text
        volume_d = get_decimal_from_currency_string(volume)
        price = tr.findAll('span',{'class':'price'})[0].text
        price_d = get_decimal_from_currency_string(price)
        percentage = tr.findAll('td',{'class':'text-right'})[2].text
        link = tr.findAll('a',{'target':'_blank'})[0]['href']
        for td in tds:
            if "Recently" in td.text:
                recently_exists = True
        if recently_exists and volume_d >= minimum_requirement_for_volume :
            #print("\t\t{} {} {}".format(volume,price,percentage))
            if price_d <= lowerest_price_to_buy:
                lowerest_price_link = link
            lowerest_price_to_buy = min(lowerest_price_to_buy,price_d)
            if price_d >= highest_price_to_sell:
                highest_price_link = link
            highest_price_to_sell = max(highest_price_to_sell,price_d)
    diff = highest_price_to_sell - lowerest_price_to_buy
    coin_markets_abs[coin] = diff
    coin_markets_per[coin] = diff / standard_price
    coin_to_links[coin] = [lowerest_price_link,highest_price_link]

import operator
sorted_coin_markets_abs = sorted(coin_markets_abs.items(), key=operator.itemgetter(1),reverse=True)
sorted_coin_markets_per = sorted(coin_markets_per.items(), key=operator.itemgetter(1),reverse=True)

abs_txt = open('abs_txt','w+')
for (coin,diff) in sorted_coin_markets_abs:
    abs_txt.write("{} {} {}\n".format(coin,diff,coin_to_links[coin]))
abs_txt.close()

per_txt = open('per_txt','w+')
for (coin,per) in sorted_coin_markets_per:
    per_txt.write("{} {}% {}\n".format(coin,per,coin_to_links[coin]))
per_txt.close()
