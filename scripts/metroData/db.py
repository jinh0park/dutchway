import django
from django.db.utils import IntegrityError
from django.conf import settings
from metro.settings import DATABASES, ASSET_DIR
from . import api
import json,os


settings.configure(
    DATABASES=DATABASES,
    INSTALLED_APPS=[
        'seoul',
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
