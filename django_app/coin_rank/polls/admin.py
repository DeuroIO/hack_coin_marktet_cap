from django.contrib import admin

from .models import *


class CoinAdmin(admin.ModelAdmin):
    list_display = ('coin_name','sector','tech','star','investment_memo','created_at','updated_at')
    search_fields = ['coin_name','sector',]


class HistoricalAdmin(admin.ModelAdmin):
    list_display = ('coin_id','daily_timestamp','average_price','volume','circulating_cap','total_cap','created_at','updated_at')
    search_fields = ['coin_id__coin_name', 'daily_timestamp', ]

class RankAdmin(admin.ModelAdmin):
    list_display = ('coin_id','daily_timestamp','rank','created_at','updated_at')
    search_fields = ['coin_id__coin_name','daily_timestamp__daily_timestamp']

class TimeStampAdmin(admin.ModelAdmin):
    list_display = ('daily_timestamp','created_at','updated_at')
    search_fields = ['daily_timestamp',]

class Price_ChangeStampAdmin(admin.ModelAdmin):
    list_display = ('coin_id','daily_timestamp','price_change','created_at','updated_at')
    search_fields = ['daily_timestamp','price_change']

admin.site.register(Coin,CoinAdmin)
admin.site.register(Historical,HistoricalAdmin)
admin.site.register(Rank,RankAdmin)
admin.site.register(Price_Change,Price_ChangeStampAdmin)
admin.site.register(TimeStamp,TimeStampAdmin)