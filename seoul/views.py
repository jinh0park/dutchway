from django.shortcuts import render
from django.views.generic import ListView
from .models import *

def index(request):
    context = {}
    return render(request, 'seoul/index.html',context)


def line_list(request):
    context = {
        'lines': Station.STATION_NUM_CHOICES
    }
    return render(request, 'seoul/lines.html',context)


def station_list(request, line_num):
    s = Station.objects.filter(line_num=line_num)
    context = {
        'stations': s
    }
    return render(request, 'seoul/stations.html',context)


class StationView:
    def get(self, request, station_nm):
        s = Station.objects.filter(station_nm=station_nm)


# Create your views here.
