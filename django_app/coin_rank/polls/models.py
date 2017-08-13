from django.db import models


class Coin(models.Model):
    def __str__(self):
        return self.coin_name + " " + self.coin_symbol
    coin_name = models.CharField(max_length=1024)
    coin_symbol = models.CharField(max_length=1024)
    sector = models.CharField(max_length=1024)
    tech = models.CharField(max_length=1024)
    star = models.IntegerField(default=-1)
    investment_memo = models.TextField()


class Historical(models.Model):
    def __str__(self):
        return self.coin_id + " " + self.total_cap
    coin_id = models.ForeignKey(Coin, on_delete=models.CASCADE)
    daily_timestamp = models.DateTimeField()
    votes = models.IntegerField(default=0)
    average_price = models.FloatField()
    volume = models.FloatField()
    circulating_cap = models.FloatField()
    total_cap = models.FloatField()

class Rank(models.Model):
    def __str__(self):
        return self.coin_id + " " + self.rank
    coin_id = models.ForeignKey(Coin,on_delete=models.CASCADE)
    daily_timestamp = models.DateTimeField()
    rank = models.IntegerField()

class Price_Change(models.Model):
    def __str__(self):
        return self.coin_id + " " + self.price_change
    coin_id = models.ForeignKey(Coin,on_delete=models.CASCADE)
    daily_timestamp = models.DateTimeField()
    price_change = models.IntegerField()