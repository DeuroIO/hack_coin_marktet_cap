from django.contrib import admin

from .models import *


class CoinAdmin(admin.ModelAdmin):
    list_display = ('coin_name','image','sector','tech','star','investment_memo','contract_address','created_at','updated_at')
    search_fields = ['coin_name','sector',]


class HistoricalAdmin(admin.ModelAdmin):
    list_display = ('coin_id','daily_timestamp','average_price','volume','circulating_cap','total_cap','created_at','updated_at')
    search_fields = ['coin_id','daily_timestamp', ]

class RankAdmin(admin.ModelAdmin):
    list_display = ('coin_id','daily_timestamp','rank','created_at','updated_at')
    search_fields = ['coin_id__coin_name','daily_timestamp__daily_timestamp']

class TimeStampAdmin(admin.ModelAdmin):
    list_display = ('id','daily_timestamp')
    search_fields = ['daily_timestamp',]

class Price_ChangeStampAdmin(admin.ModelAdmin):
    list_display = ('coin_id','daily_timestamp','price_change','created_at','updated_at')
    search_fields = ['daily_timestamp','price_change']

class AccountAdmin(admin.ModelAdmin):
    list_display = ('gussed_name','account_address')
    search_fields = ['account_address','gussed_name']

class TokenTransactionAdmin(admin.ModelAdmin):
    list_display = ('token_name','tx_hash','timestamp','from_account','to_account','quantity')
    search_fields = ['token_name','tx_hash','timestamp','from_account','to_account','quantity']


admin.site.register(Coin,CoinAdmin)
admin.site.register(Historical,HistoricalAdmin)
admin.site.register(Rank,RankAdmin)
admin.site.register(Price_Change,Price_ChangeStampAdmin)
admin.site.register(TimeStamp,TimeStampAdmin)
admin.site.register(Account,AccountAdmin)
admin.site.register(TokenTransaction,TokenTransactionAdmin)
