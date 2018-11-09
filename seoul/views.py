from django.shortcuts import render, reverse
from django.views.generic import ListView
from .models import *
import numpy as np
from metro.settings import BASE_DIR
import os, json
from django.http import Http404, JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods

def index(request):
    context = {}
    return render(request, 'seoul/index.html',context)

@require_http_methods(["POST"])
def filter(request):
    station = []
    station_nm = []
    print(request.POST.dict())
    for item in request.POST.dict().items():
        try:
            if item[0].split("-")[0] == 'station':
                s = Station.objects.filter(station_nm=item[1])[0]
                station.append(s.fr_code)
                station_nm.append(item[1])
        except:
            pass
    print(station)
    station_text = ""
    station_nm_text = ""
    for s,nm in zip(station,station_nm):
        station_text+=s+','
        station_nm_text+=nm+' '

    station_text = station_text[:-1]
    print(station_text)
    context = {
        'station':station_text,
        'station_nm': station_nm_text
    }
    return render(request, 'seoul/filter.html',context)


@require_http_methods(["POST"])
def pathfinder(request):
    try:
        p = request.POST

        s = p.get('station').split(',')
        if len(s) <=1:
            raise Exception
        avg_f = int(p.get("avg")) if p.get("avg") else 1000
        max_f = int(p.get("max")) if p.get("max") else 1000
        transfer_f = int(p.get("trans")) if p.get("trans") else 1000
        sub_f = int(p.get("sub")) if p.get("sub") else 1000
        order = int(p.get("order")) if p.get("order") else 'max'
        ret = func(stations_fr_code = s, avg_f=avg_f, max_f=max_f, transfer_f=transfer_f, sub_f=sub_f, order=order)

        cnt = 10
        if p.get("count"):
            cnt = min(int(p.get("count")),10) # 최대 10개

        #ret = ret[:cnt]

        response = {
            "status": 200,
            "content" : ret
        }
        return JsonResponse(response)
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()






def func(stations_fr_code, avg_f=1000, max_f=1000, transfer_f=1000, sub_f=1000, order='tag_count'):
    file = os.path.join(BASE_DIR,'seoul','asset', 'shortest_path.npy')
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
                'tag_count':dest.tag_count
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
    rett.reverse()
    return rett


# Create your views here.
