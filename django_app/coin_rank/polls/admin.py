from django.contrib import admin

from .models import *

admin.site.register(Coin)
admin.site.register(Historical)
admin.site.register(Rank)
admin.site.register(Price_Change)