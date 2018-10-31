#django db에 접근하는 기능들을 작성하는 파일
import django
from django.db.utils import IntegrityError
from django.conf import settings
from metro.settings import DATABASES, ASSET_DIR, BASE_DIR
from . import api
from ._config import api_key
import json,os
import requests


settings.configure(
    DATABASES=DATABASES,
    INSTALLED_APPS=[
        'seoul.apps.SeoulConfig',
    ]
)
django.setup()

from seoul.models import Station



def update_metro_db(recent=False):
    if recent:
        api.update_metro_json_file()
    try:
        with open(os.path.join(ASSET_DIR, 'seoul_metro_all.json'),'r',encoding='utf-8') as f:
            data = json.loads(f.read())
            count = data['SearchSTNBySubwayLineService']['list_total_count']
            c = 0
            m = 0
            for station in data['SearchSTNBySubwayLineService']['row']:
                try:
                    Station.objects.create(
                        line_num= station['LINE_NUM'],
                        station_cd=station['STATION_CD'],
                        station_nm=station['STATION_NM'],
                        fr_code=station['FR_CODE']
                    )
                    c += 1
                except IntegrityError:
                    s = Station.objects.get(station_cd=station['STATION_CD'])
                    if((s.line_num, s.station_nm, s.fr_code)
                            == tuple([station[index] for index in ('LINE_NUM', 'STATION_NM', 'FR_CODE')])):
                        pass
                    else:
                        s.line_num=station['LINE_NUM'],
                        s.station_cd=station['STATION_CD'],
                        s.station_nm=station['STATION_NM'],
                        s.fr_code=station['FR_CODE']
                        m += 1


            print("DB Updated.({} created / {} modified / {} total)".format(c, m, count))
            return True

    except FileNotFoundError:
        print("There is no metro json file, Please update / download the file first.")
        return False


def download_station_json(staion_nm):
    url = 'http://swopenapi.seoul.go.kr/api/subway/{}/json/stationInfo/0/5/{}'.format(api_key, staion_nm)
    res = requests.get(url)
    if res.status_code == 200:
        with open(os.path.join(ASSET_DIR, 'seoul_metro_station_json', '{}.json'.format(staion_nm)), 'w', encoding='utf-8') as w:
            w.write(res.text)
            print("Updated Successfully.")
            return True
    else:
        print("Update Failed: Error {}".format(res.status_code))
        return False


def download_station_json_all():
    stations = Station.objects.all()
    n = len(stations)
    cnt = 0
    while cnt < n:
        station_nm = stations[cnt]
        if download_station_json(station_nm):
            print(station_nm)
            cnt += 1

def update_station_transfer_num():
    for station in Station.objects.all():
        try:
            station.transfer_count = Station.objects.filter(station_nm=station.station_nm).count()
            station.save()
            print(station.station_nm, station.transfer_count)
        except Exception as e:
            print(e)
            pass


def get_adjacent_station(station_nm, line_num):
    line_name = dict(Station.STATION_NUM_CHOICES).get(line_num)

    with open(os.path.join(ASSET_DIR, 'seoul_metro_station_json', station_nm + '.json'), encoding='utf-8') as f:
        data = json.loads(f.read())
        if 'stationList' not in data:
            print('해당 역에 대한 정보가 없습니다: {}'.format(station_nm))
            return False
        stationList = data['stationList']
        for s in stationList:
            if s['subwayNm'] == line_name:
                return (s['statnFnm'], s['statnTnm'])
        print('데이터 오류')
        return False

def set_adjacent_station():
    for station in Station.objects.all():
        try:
            r = get_adjacent_station(station.station_nm, station.line_num)
            if r:
                station.tail_station, station.head_station = [Station.objects.get(station_nm=name,
                                                                                  line_num=station.line_num) for name in r]
                station.save()
                print("완료", station.station_nm)
            else:
                print("정보없음", station.station_nm)
        except Exception as e:
            print("error", str(e))
            pass




def get_line_name_by_num(line_num):
    return dict(Station.STATION_NUM_CHOICES).get(line_num)

def update_naver_cd_station():
    with open(os.path.join(BASE_DIR, 'scripts', '3.txt'), 'r', encoding='utf-8') as f:
        r = f.readlines()
        cnt= 0
        for line in r:
            line = line.strip()
            if line:
                name, fr, naver = line.split('|')
                s = Station.objects.get(fr_code=fr)
                s.naver_cd = naver
                s.save()
                cnt+=1
                print(line)
    print('{}개 완료'.format(cnt))


