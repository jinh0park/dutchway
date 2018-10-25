import os, json
from metro.settings import ASSET_DIR

with open(os.path.join(ASSET_DIR,'/seoul_metro_all.json'),'r',encoding='utf-8') as f:
    data = json.loads(f.read())
    for station in data['SearchSTNBySubwayLineService']['row']:
        if(station['LINE_NUM'] == '3'):
            print(station)
