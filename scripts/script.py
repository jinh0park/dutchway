from scripts.metroData import api as metroApi
from scripts.metroData import db as metroDB
from scripts.metroData import crawl as metroCrawl
from scripts.metroData import pathfinder as metroPath
from django.db.models import Q
import time

#metroApi.update_metro_json_file()
#metroDB.update_metro_db()
#metroDB.download_station_json_all()
#metroDB.update_station_transfer_num()
#print(metroDB.get_adjacent_station('교대','2'))
#print(metroCrawl.get_naver_subway_code('평택역', '1호선'))
#print(metroDB.Station.objects.all().count())
#metroDB.update_naver_cd_station()
# metroDB.set_adjacent_station()

# for i in metroDB.Station.STATION_NUM_CHOICES:
#     metroCrawl.get_path_time_adjacent_station(i[0])

#metroPath.save_shortest_path_array()
# metroPath.shortest_path_by_fr_code(1,1)
#metroPath.equal_path_by_fr_code('228','344')
metroCrawl.instagram_tag_count_update()




def naver_code_func():
    with open('output.txt','w',encoding='utf=8') as f:
        stations = metroDB.Station.objects.filter(naver_cd='')
        for station in stations:
            try:
                name = station.station_nm
                line = metroDB.get_line_name_by_num(station.line_num)
                r = metroCrawl.get_naver_subway_code(name+'역', line)
                t = '{}|{}|{}'.format(station.station_nm, station.fr_code, r)
                print(t)
                f.write(t+'\n')
            except Exception as e:
                print('error: '+str(e))
                pass
