import django_tables2 as tables
from .models import Coin

class BootstrapTable(tables.Table):
    Link = tables.TemplateColumn('<a href="/coin?id={{record.id}}">details</a>')
    Rank = tables.Column(accessor='rank.daily_timestamp.daily_timestamp')
    class Meta:
        model = Coin
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-bordered table-striped table-hover'}
        exclude = ('id','investment_memo','created_at','updated_at')
        sequence = ('Rank','Link', 'coin_name', 'sector','tech','star')