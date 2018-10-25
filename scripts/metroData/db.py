import django
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
            try:
                for station in data['SearchSTNBySubwayLineService']['row']:
                    Station.objects.create(
                        line_num= station['LINE_NUM'],
                        station_cd=station['STATION_CD'],
                        station_nm=station['STATION_NM'],
                        fr_code=station['FR_CODE']
                    )
                print("DB Updated Successfully.")
                return True

            except Exception as e:
                print(e)

    except FileNotFoundError:
        print("There is no metro json file, Please update / download the file first.")
        return False
