
from datetime import datetime
from collections import namedtuple
from itertools import groupby

RainDataPoint = namedtuple('RainDataPoint', 'date_recorded, daily_total, hourly_data')

#this strips everything after the line of --------------- in the file by
def remove_header(data):
    for line_number, line in enumerate(data):
        #creates '-' as set - since set type cannot have dupe values, the line of ----- becomes a set of one -.
        #this returns all data after the line number +1 (line number starts at 0, hence the +1)
        if set(line.strip()) == {'-'}:
            return data[line_number + 1:]


def parse_rain_data(rain_data):

    #create two lists to hold data
    all_data = list()
    rain_data = rain_data.split('\n')
    #runs remove_header() created above
    rain_data = remove_header(rain_data)
    #splits data by default of split() - white space. then strips out strings of white space using strip
    #if it finds a ''-' as a data entry it will skip the entire line it is in
    for data in rain_data:
        clean_data = data.split()
        clean_data = [data.strip() for data in clean_data]
        # print(len(clean_data))
        if '-' in clean_data or len(clean_data) <= 2:
            continue

        #creates a recognizable date with the dateimte function
        date = clean_data[0]

        try:
            date = datetime.strptime(date, '%d-%b-%Y')
        except ValueError:
            continue


        #creates daily total by slicing at position
        daily_total = int(clean_data[1])

        #creates hourly total by slicing all after 2nd position
        hourly_totals = clean_data[2:]

        #transfers data to named tuple, save to list above
        rain_data_point = RainDataPoint._make((date, daily_total, hourly_totals))
        all_data.append(rain_data_point._asdict())
        #RainDataPoint(date_recorded=datetime.datetime(2016, 3, 30, 0, 0), daily_total='0', hourly_data=['0', '0', '0',])

    return all_data
#creates variable that will run parse function on file
# data = parse_rain_data('sample.rain')
#
# #Tell it which field of named tuple to pull data for max to compare. Create variable with day and amount.
# max_daily_rain = max(data, key=lambda d: d.daily_total)
# max_rain_day = max_daily_rain[0]
# max_rain = max_daily_rain[1]
#
# #prints day with most rain in data set
# print(f"The most rain Portland has seen since 2002 was on {max_rain_day.strftime('%x')}. It rained {max_rain / 100} inches that day!")
#
# #this sorts data by date
# max_rain_year = sorted(data, key=lambda d: d.date_recorded)
#
# #this groups each date by year
# rainfall_by_year = groupby(max_rain_year, key=lambda d: d.date_recorded.year)
#
# #this creates a dictionary. takes
# year_dictionary = {k : sum(v.daily_total for v in g) for k, g in rainfall_by_year}
#
# max_year = max(year_dictionary, key=year_dictionary.get)
# print(f"The year with the most rainfall was {max_year}.")
