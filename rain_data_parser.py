from collections import namedtuple
from datetime import datetime
from itertools import groupby

RainDataLocation = namedtuple('RainDataLocation', 'name, location, count, rain_data')
RainDataPoint = namedtuple('RainDataPoint', 'date_recorded, daily_total, hourly_data')

def get_header_info(data):
    return [value.strip() for value in data[0].split('-')]


def remove_header(data):
    for line_number, line in enumerate(data):
        if set(line.strip()) == {'-'}:
            return data[line_number + 1:]

def parse_rain_data(rain_data):
    all_data = list()

    rain_data = remove_header(rain_data)

    for data in rain_data[1:]:
        clean_data = data.split()
        clean_data = [data.strip() for data in clean_data]

        if '-' in clean_data or len(clean_data) <= 2:
            continue

        try:
            date = clean_data[0]
            date = datetime.strptime(date, '%d-%b-%Y')
        except ValueError:
            continue
        else:
            daily_total = int(clean_data[1])
            hourly_totals = clean_data[2:]

        rain_data_point = RainDataPoint._make((date, daily_total, hourly_totals))._asdict()
        all_data.append(rain_data_point)

    return all_data
