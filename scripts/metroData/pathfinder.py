from scipy.sparse.csgraph import shortest_path
from .db import Station
import numpy as np
from django.db.models import Q
np.set_printoptions(threshold=np.inf)
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
        ret[s.index][s_.index] = 3


y = shortest_path(ret)


for i, x in enumerate(y[117,:]):
    print(x,Station.objects.get(index=i))
