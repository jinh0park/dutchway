from django.shortcuts import render, reverse
from django.views.generic import ListView
from .models import *
import numpy as np
import os, json
from metro.settings import ASSET_DIR
from django.http import Http404, JsonResponse, HttpResponseBadRequest

def index(request):
    context = {}
    return render(request, reverse('seoul:index'),context)


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



def pathfinder(request):
    if request.method != 'GET':
        return Http404()
    try:
        s = request.GET.get('station').split(',')
        if len(s) <=1:
            raise Exception
        avg_f = int(request.GET.get("avg")) if request.GET.get("avg") else 1000
        max_f = int(request.GET.get("max")) if request.GET.get("max") else 1000
        transfer_f = int(request.GET.get("trans")) if request.GET.get("trans") else 1000
        sub_f = int(request.GET.get("sub")) if request.GET.get("sub") else 1000
        order = int(request.GET.get("order")) if request.GET.get("order") else 'max'
        ret = func(stations_fr_code = s, avg_f=avg_f, max_f=max_f, transfer_f=transfer_f, sub_f=sub_f, order=order)
        if request.GET.get("count"):
            cnt = int(request.GET.get("count"))
            ret = ret[:cnt]
        response = {
            "status": 200,
            "content" : ret
        }
        return JsonResponse(response)
    except:
        return HttpResponseBadRequest()






def func(stations_fr_code, avg_f=1000, max_f=1000, transfer_f=1000, sub_f=1000, order='max'):
    file = os.path.join(ASSET_DIR, 'shortest_path.npy')
    path = np.load(file)
    indices = [Station.objects.get(fr_code=fr_code).index for fr_code in stations_fr_code]
    N = path.shape[0]
    t = []
    trans = []
    f = []
    for i in range(N):
        t.append([int(path[index, i]) for index in indices])
        trans.append([int(round(path[index, i] * 100)) % 100 for index in indices])
        f.append(False)

    t_arr = np.array(t)
    trans_arr = np.array(trans)

    avg_arr = np.average(t_arr, axis=1)
    max_arr = np.max(t_arr, axis=1)
    transfer_arr = np.max(trans_arr, axis=1)
    sub_arr = np.abs(np.max(t_arr, axis=1) - np.min(t_arr, axis=1))

    for i in range(N):
        f[i] = avg_arr[i] < avg_f and max_arr[i] < max_f and transfer_arr[i] < transfer_f and sub_arr[i] < sub_f

    ret = []
    for i in range(N):
        if f[i]:
            dest = Station.objects.get(index=i)
            dest_ = {
                'station_nm': dest.station_nm,
                'line_num':dest.line_num,
                'fr_code':dest.fr_code,
                'naver_cd':dest.naver_cd,
            }
            tmp = {
                'dest': dest_,
                'time': t[i],
                'trans':trans[i],
                'avg': int(avg_arr[i]),
                'max': int(max_arr[i]),
                'trans_max': int(transfer_arr[i]),
                'sub_max': int(sub_arr[i])
            }
            ret.append(tmp)

    rett = sorted(ret, key=lambda x: x[order])
    return rett


# Create your views here.
