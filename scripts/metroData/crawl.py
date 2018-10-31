from selenium import webdriver
from metro.settings import BASE_DIR
import os, time
from urllib.parse import urlparse,parse_qs

def driver_on():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome(os.path.join(BASE_DIR,'scripts','metroData','webdriver','chromedriver.exe'), chrome_options=options)
    driver.implicitly_wait(3)
    return driver


def get_path_time(fr_code_departure, fr_code_arrival):
    if fr_code_arrival == fr_code_departure:
        return 0
    driver = driver_on()
    driver.get('https://m.map.naver.com/viewer/subwayPath.nhn?region=1000&departureId={}&arrivalId={}&pathType=1'.format(fr_code_departure,fr_code_arrival))
    x = driver.find_element_by_class_name('_time')
    if x is None:
        return 0
    print(x.text)
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