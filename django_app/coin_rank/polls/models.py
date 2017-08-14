from django.db import models


class Coin(models.Model):
    def __str__(self):
        return self.coin_name + " "
    def get_id(self):
        return self.id
    def get_rank_at(self,timestamp):
        try:
            r = Rank.objects.get(daily_timestamp=timestamp, coin_id=self)
            return r.rank
        except:
            return -1
    coin_name = models.CharField(max_length=1024)
    sector = models.CharField(max_length=1024)
    tech = models.CharField(max_length=1024)
    star = models.IntegerField(default=-1)
    investment_memo = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TimeStamp(models.Model):
    def __str__(self):
        return self.daily_timestamp.strftime('%b %d, %Y')
    daily_timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Historical(models.Model):
    def __str__(self):
        return self.coin_id.coin_name + " " + str(self.total_cap) + " at " + self.daily_timestamp.daily_timestamp.strftime('%b %d, %Y')
    coin_id = models.ForeignKey(Coin, on_delete=models.CASCADE)
    daily_timestamp = models.ForeignKey(TimeStamp)
    average_price = models.FloatField()
    volume = models.FloatField()
    circulating_cap = models.FloatField()
    total_cap = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Rank(models.Model):
    def __str__(self):
        return self.coin_id.coin_name + " " + str(self.rank) + " at " + self.daily_timestamp.daily_timestamp.strftime('%b %d, %Y')
    coin_id = models.ForeignKey(Coin,on_delete=models.CASCADE)
    daily_timestamp = models.ForeignKey(TimeStamp)
    rank = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Price_Change(models.Model):
    def __str__(self):
        return self.coin_id.coin_name + " " + str(self.price_change) + " at " + self.daily_timestamp.daily_timestamp.strftime('%b %d, %Y')
    coin_id = models.ForeignKey(Coin,on_delete=models.CASCADE)
    daily_timestamp = models.ForeignKey(TimeStamp)
    price_change = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)