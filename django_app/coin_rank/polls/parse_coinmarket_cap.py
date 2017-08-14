import urllib
from bs4 import BeautifulSoup
import sys
from re import sub
from decimal import Decimal
import datetime

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

