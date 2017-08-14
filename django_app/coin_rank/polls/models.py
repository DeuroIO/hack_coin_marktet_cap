from django.db import models


class Coin(models.Model):
    def __str__(self):
        return self.coin_name + " "
    def get_id(self):
        return self.id
    coin_name = models.CharField(max_length=1024)
    sector = models.CharField(max_length=1024)
    tech = models.CharField(max_length=1024)
    star = models.IntegerField(default=-1)
    investment_memo = models.TextField()


class Historical(models.Model):
    def __str__(self):
        return self.coin_id.coin_name + " " + str(self.total_cap) + " at " + self.daily_timestamp.strftime('%b %d, %Y')
    coin_id = models.ForeignKey(Coin, on_delete=models.CASCADE)
    daily_timestamp = models.DateTimeField()
    average_price = models.FloatField()
    volume = models.FloatField()
    circulating_cap = models.FloatField()
    total_cap = models.FloatField()

class Rank(models.Model):
    def __str__(self):
        return self.coin_id.coin_name + " " + str(self.rank) + " at " + self.daily_timestamp.strftime('%b %d, %Y')
    coin_id = models.ForeignKey(Coin,on_delete=models.CASCADE)
    daily_timestamp = models.DateTimeField()
    rank = models.IntegerField()

class Price_Change(models.Model):
    def __str__(self):
        return self.coin_id.coin_name + " " + str(self.price_change) + " at " + self.daily_timestamp.strftime('%b %d, %Y')
    coin_id = models.ForeignKey(Coin,on_delete=models.CASCADE)
    daily_timestamp = models.DateTimeField()
    price_change = models.IntegerField()