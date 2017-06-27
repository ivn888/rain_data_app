import os
import json
import requests

from bs4 import BeautifulSoup
from datetime_json import DateTimeEncoder, DateTimeDecoder
from pprint import pprint

from print_colors import wrap_color as pwc
from rain_data_parser import RainDataLocation, parse_rain_data, get_header_info


DEFAULT_CACHE_FILE = 'cache.json'
SOURCE_URL = 'https://or.water.usgs.gov/non-usgs/bes/'

def get_rain_urls(url):
    request_data = requests.get(url)

    html_data = BeautifulSoup(request_data.text, 'html.parser')
    links = html_data.find_all('a')

    if url[-1] != '/':
        url = url + '/'

    links = [url + link['href'] for link in links if '.rain' in link['href']]

    return links

def crawl_rain_tables(links):
    rain_tables = dict()

    for link in links:
        print(f'{pwc("process", "Retrieving file ")}{pwc("attention", " @ ")}{pwc("happening", " " + link)}...')

        request_data = requests.get(link)

        if request_data.status_code != 200:
            continue

        request_data = request_data.text.split('\n')

        name = 'Unknown'
        header_info = get_header_info(request_data)

        if len(header_info) == 2:
            name, location = header_info
        else:
            location = header_info[0]

        rain_data = parse_rain_data(request_data)
        rain_data_location = RainDataLocation(name=name, location=location, count=len(rain_data), rain_data=rain_data)
        print(f'{pwc("about", rain_data_location.name + " ")}{pwc("success", " " + rain_data_location.location) + " "}')
        rain_tables[link] = rain_data_location._asdict()

    return rain_tables


def cache_rain_tables(rain_tables, output_file=DEFAULT_CACHE_FILE):
    with open(output_file, 'w+') as f:
        f.write(json.dumps(['rain_data_cache', rain_tables], cls=DateTimeEncoder))


def load_cached_rain_tables(input_file=DEFAULT_CACHE_FILE):
    with open(input_file, 'r') as f:
        rain_location_data = json.loads(f.read(), object_hook=DateTimeDecoder.decode)[1]
        rain_locations = [value for key, value in rain_location_data.items()]
        return rain_locations

def get_location_data(rain_data, _location, year):
    for location in rain_data:
        if location['location'].casefold() != _location.casefold():
            continue
        location_data = list(filter(lambda d: d['date_recorded']['val'].year == year, location['rain_data']))
        if len(location_data) > 0:
            if len(location['rain_data']) > 360:
                return location_data
        else:
            raise ValueError('no location data found for year')

def average_daily_rain_total_per_year_by_location(rain_data, location, year):
    rain_data_location = get_location_data(rain_data, location, year)
    daily_average = sum(d['daily_total'] for d in rain_data_location) / 365
    daily_average /= 100
    return daily_average

def number_rainy_days(rain_data, year):
    data = list()
    len_valid_locations = len(rain_data)
    for location in rain_data:
        if len(location['rain_data']) < 350:
            len_valid_locations -= 1
            continue
        location_data = list(filter(lambda d: d['date_recorded']['val'].year == year, location['rain_data']))
        data += [location_data]

    count = 0

    for location in data:
        for day in location:
            if day['daily_total'] > 0:
                count += 1
    return count / len_valid_locations

if not os.path.exists(DEFAULT_CACHE_FILE) and not os.path.isfile(DEFAULT_CACHE_FILE):
    rain_table_urls = get_rain_urls(SOURCE_URL)
    print('-' * 50)
    print(f'Retrieving .rain files from specified source... (eg. "{SOURCE_URL}")')
    print('-' * 50 + '\n')
    rain_tables = crawl_rain_tables(rain_table_urls)
    cache_rain_tables(rain_tables)

cached_data = load_cached_rain_tables()
average_daily_rain_total_per_year_by_location(cached_data, '10351 NW. Thompson Rd.', 2016)
number_rainy_days(cached_data, 2016)

year_range = range(2010, 2017)
count = 0
for year in year_range:
    # print(number_rainy_days(cached_data, year))
    count += number_rainy_days(cached_data, year)

print(count / len(year_range))


# HOW TO STORE THIS DATA FOR USE LATER >>>> HINT: LOOK INTO CSVS
