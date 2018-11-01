from selenium import webdriver
from metro.settings import BASE_DIR
import os, time
from urllib.parse import urlparse,parse_qs
from . import db as metroDB

def driver_on():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("disable-gpu")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

    driver = webdriver.Chrome(os.path.join(BASE_DIR,'scripts','metroData','webdriver','chromedriver.exe'), chrome_options=options)
    driver.implicitly_wait(3)
    return driver


def get_path_time(naver_code_departure, naver_code_arrival):
    if naver_code_arrival == naver_code_departure:
        return 0
    driver = driver_on()
    driver.get('https://m.map.naver.com/viewer/subwayPath.nhn?region=1000&departureId={}&arrivalId={}&pathType=1'.format(naver_code_departure,naver_code_arrival))
    time.sleep(1)
    x = driver.find_element_by_class_name('_time')
    if x is None:
        return 0
    print(x.text)
    driver.quit()
    return int(x.text[:-1])


def get_naver_subway_code(station_nm, line_name):
    driver = driver_on()
    driver.get('https://m.map.naver.com/search2/search.nhn?query={}%20{}'.format(station_nm, line_name))
    x = driver.find_element_by_class_name('_item').find_element_by_class_name('_title')
    x.click()
    time.sleep(2)
    u = urlparse(driver.current_url)
    q = parse_qs(u.query)
    driver.quit()
    return q.get('stationId')[0]

def get_path_time_adjacent_station(line_num):
    driver = driver_on()
    for s in metroDB.Station.objects.filter(line_num=line_num):
        if s.naver_cd == s.head_station.naver_cd:
            continue
        driver.get(
            'https://m.map.naver.com/viewer/subwayPath.nhn?region=1000&departureId={}&arrivalId={}&pathType=1'.format(
                s.naver_cd, s.head_station.naver_cd))
        time.sleep(1)
        x = driver.find_element_by_class_name('_time')
        if x is None:
            return 0
        print(x.text)
    driver.quit()

