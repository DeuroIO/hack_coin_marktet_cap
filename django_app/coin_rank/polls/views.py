from django.http import HttpResponse
from django.shortcuts import render_to_response


def index(request):
    return render_to_response('index.html')

def detail(request, coin_id):
    return HttpResponse("You're looking at coin %s." % coin_id)