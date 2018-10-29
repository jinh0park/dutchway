from scripts.metroData import api as metroApi
from scripts.metroData import db as metroDB

#metroApi.update_metro_json_file()
#metroDB.update_metro_db()
#metroDB.download_station_json_all()
metroDB.update_station_transfer_num()
