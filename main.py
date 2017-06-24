import requests
from bs4 import BeautifulSoup
from make_it_rain import parse_rain_data
import json
from datetime_encoder import DateTimeEncoder

def get_rain_urls(url):
    request_data = requests.get(url)
    html_data = BeautifulSoup(request_data.text, "html.parser")
    links = html_data.find_all("a")

    if url[-1] != "/":
        url = url + "/"

    links = [url + link['href'] for link in links if '.rain' in link['href']]

    return links

# get_rain_urls('https://or.water.usgs.gov/non-usgs/bes/')

def crawl_rain_tables(links):
    rain_tables = dict()
    for link in links:
        if len(rain_tables.keys()) > 2:
            break
        print(link)
        request_data = requests.get(link)

        if request_data.status_code != 200:
            continue

        # rain_tables.append(parse_rain_data(request_data.text))

        rain_tables[link] = parse_rain_data(request_data.text)

    return(rain_tables)


def cache_rain_tables(rain_tables, output_file='cache.json'):
    with open(output_file, 'w+') as f:
        f.write(json.dumps(['rain_data_cache', rain_tables], cls=DateTimeEncoder))


rain_table_urls = get_rain_urls('https://or.water.usgs.gov/non-usgs/bes/')
rain_data = crawl_rain_tables(rain_table_urls)
cache_rain_tables(rain_data)

# HOW TO STORE THIS DATA FOR USE LATER >>>> HINT: LOOK INTO CSVS
