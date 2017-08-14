import django_tables2 as tables
from .models import Coin

class BootstrapTable(tables.Table):
    Link = tables.TemplateColumn('<a href="/coin?id={{record.id}}">details</a>')
    class Meta:
        model = Coin
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-bordered table-striped table-hover'}
        exclude = ('friendly', )