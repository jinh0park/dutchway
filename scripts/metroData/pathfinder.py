from scipy.sparse.csgraph import shortest_path
from metro.settings import ASSET_DIR
from .db import Station
import numpy as np
from django.db.models import Q
import os


def find_shortest_path():
    N = Station.objects.all().count()
    ret = np.zeros((N,N))
    inf = 9999.0
    ret.fill(inf)

    S = Station.objects.all()
    # 인접 역 간 소요시간
    for s in S:
        h = s.head_time
        ret[s.index, s.head_station.index] = s.head_time if s.head_time is not None else inf
        t = s.tail_time
        ret[s.index, s.tail_station.index] = s.tail_time if s.tail_time is not None else inf
    # 같은 역은 0분
    for i in range(N):
        ret[i,i] = 0
    # 환승하는 시간 (일단 5분으로 설정)
    for s in Station.objects.filter(transfer_count__gte=2):
        S_ = Station.objects.filter(station_nm=s.station_nm).exclude(station_cd=s.station_cd)
        for s_ in S_:
            ret[s.index][s_.index] = 3.01

    y = shortest_path(ret)
    return y

def save_shortest_path_array():
    try:
        file = os.path.join(ASSET_DIR, 'shortest_path.npy')
        np.save(file,find_shortest_path())
        print("Shortest path array saved successfully.")
        return True
    except:
        print("Error occurred while save array")
        return False


def shortest_path_by_fr_code(s1, s2):
    file = os.path.join(ASSET_DIR, 'shortest_path.npy')
    path = np.load(file)
    i1 = Station.objects.get(fr_code=s1).index
    i2 = Station.objects.get(fr_code=s2).index
    return path[i1,i2]

def equal_path_by_fr_code(s1, s2, sub_threshold=10, sum_threshold=1000):
    file = os.path.join(ASSET_DIR, 'shortest_path.npy')
    path = np.load(file)
    i1 = Station.objects.get(fr_code=s1).index
    i2 = Station.objects.get(fr_code=s2).index
    p1 = path[i1,:]
    p2 = path[i2,:]
    sums = p1+p2
    subs = np.abs(p1-p2)
    ret = []
    for i, (sum, sub)in enumerate(zip(sums, subs)):
        if sum > sum_threshold:
            continue
        if sub <= sub_threshold:
            dest = Station.objects.get(index=i)
            ret.append((str(dest), round(p1[i], 2), round(p2[i], 2), round(sum, 2)))
    ret_sorted = sorted(ret, key=lambda x: x[3])
    for x in ret_sorted:
        print(x)
    return ret_sorted


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

    avg_arr = np.average(t_arr,axis=1)
    max_arr = np.max(t_arr,axis=1)
    transfer_arr = np.max(trans_arr,axis=1)
    sub_arr = np.abs(np.max(t_arr,axis=1) - np.min(t_arr,axis=1))

    for i in range(N):
        f[i] = avg_arr[i] < avg_f and max_arr[i] < max_f and transfer_arr[i] < transfer_f and sub_arr[i] < sub_f

    ret = []
    for i in range(N):
        if f[i]:
            dest = Station.objects.get(index=i).fr_code
            tmp = {
                'dest': dest,
                'time': t[i],
                'trans':trans[i],
                'avg': avg_arr[i],
                'max': max_arr[i],
                'trans_max': transfer_arr[i],
                'sub_max': sub_arr[i]
            }
            ret.append(tmp)

    rett = sorted(ret, key=lambda x: x['max'])
    return rett









