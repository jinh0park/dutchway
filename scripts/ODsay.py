import requests

def search_path(sx, sy, ex, ey):
    params = {
        'SX':sx,
        'SY':sy,
        'EX':ex,
        'EY':ey,
        'apiKey': '3JvTm/iWL7gwb4VCKcVEyg',
    }
    url = 'https://api.odsay.com/v1/api/searchPubTransPath'
    r = requests.get(url=url, params=params)
    return r.text


sy = 37.652380
sx = 126.777577
ey = 37.460170
ex = 126.951916
print(search_path(sx, sy, ex, ey))