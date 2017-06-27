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

        for location in rain_locations:
            print(f"Name: {location['name']}")
            print(f"Data Points: {location['count']}")
            for data_point in location['rain_data'][:2]:
                pass



if not os.path.exists(DEFAULT_CACHE_FILE) and not os.path.isfile(DEFAULT_CACHE_FILE):
    rain_table_urls = get_rain_urls(SOURCE_URL)
    print('-' * 50)
    print(f'Retrieving .rain files from specified source... (eg. "{SOURCE_URL}")')
    print('-' * 50 + '\n')
    rain_tables = crawl_rain_tables(rain_table_urls)
    cache_rain_tables(rain_tables)

load_cached_rain_tables()

# HOW TO STORE THIS DATA FOR USE LATER >>>> HINT: LOOK INTO CSVS
