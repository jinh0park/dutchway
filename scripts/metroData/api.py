import requests
from ._config import api_key
from metro.settings import ASSET_DIR
import os

def update_metro_json_file():
    url = 'http://openapi.seoul.go.kr:8088/{}/json/SearchSTNBySubwayLineService/1/1000'.format(api_key)
    res = requests.get(url)
    if res.status_code == 200:
        with open(os.path.join(ASSET_DIR, 'seoul_metro_all.json'),'w',encoding='utf-8') as w:
            w.write(res.text)
            print("Updated Successfully.")
            return True
    else:
        print("Update Failed: Error {}".format(res.status_code))
        return False


