import urllib
from bs4 import BeautifulSoup
import sys
from re import sub
from decimal import Decimal
import datetime
from .models import Historical,Coin, TimeStamp
from numpy import mean
import re
import pytz

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

def get_all_coins():
    base_url = 'https://coinmarketcap.com'
    soup = get_html_by_url(base_url)
    arrs = soup.findAll('td', {'class': 'no-wrap currency-name'})
    coin_to_url = dict()
    for arr in arrs:
        imgs = arr.findAll('img', {'class': 'currency-logo'})
        name = imgs[0]['alt']
        link = base_url + arr.findAll('a')[0]['href'] + "historical-data?start=20130428&end="
        coin_to_url[name] = link
    return coin_to_url

def get_historical_data_for_url(url):
    now = datetime.datetime.now()
    url = url + str(now.year)
    if now.month < 10:
        url += "0" + str(now.month)
    else:
        url += str(now.month)
    if now.day < 10:
        url += "0" + str(now.day)
    else:
        url += str(now.day)
    print(url)
    soup = get_html_by_url(url)

    #Try to calculate total_supply
    h3s = soup.findAll('h3')

    total_supply = 0
    for h3 in h3s:
        title = h3.text.lower()
        if 'supply' in title and title != 'circulating supply':
            div_parent = h3.parent.parent
            total_supply = div_parent.findAll('div',{"class":"coin-summary-item-detail"})[0].text
            total_supply = float(re.sub("[^0-9]", "", total_supply))
            break

    trs = soup.findAll("tr",{'class':'text-right'})
    timestamp_dict = dict()
    timestamp_set = set()
    for tr in trs:
        counts = 0
        values = []
        #Timestamp, Open, High, Low, Close, Volume, Mraket_Cap
        for td in tr.findAll('td'):
            if counts < 7:
                if counts == 0:
                    # timestamp
                    timestamp = datetime.datetime.strptime(td.text, "%b %d, %Y")
                    values.append(timestamp)
                elif td.text == "-":
                    values.append(0.0)
                elif "," in td.text:
                    t = td.text.replace(',','')
                    values.append(float(t))
                else:
                    values.append(float(td.text))
                counts += 1


        coin_average_price = mean(values[1:5])
        total_cap = values[-1]
        if total_supply != 0:
            total_cap = coin_average_price * total_supply

        if values[0] not in timestamp_dict:
            timestamp_set.add(values[0])
            timestamp_dict[values[0]] = {'average_price':coin_average_price,
                               'volume':values[-2], 'circulating_cap':values[-1],
                               'total_cap':total_cap}
    return timestamp_dict,timestamp_set

