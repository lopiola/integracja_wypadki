#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Parsing FARS vehicle CSV files and putting them into DB

Significant attributes:
ST_CASE - case ID
PERSONS
FATALS
VE_TOTAL - number of vehicles
YEAR
MONTH
DAY
DAY_WEEK
HOUR
MINUTE
LATITUDE
LONGITUD
"""

import csv
import sys
from db_api import accident


def get_int(list_row, index):
    return int(float(list_row[index]))


def get_float(list_row, index):
    return float(list_row[index])


if len(sys.argv) != 2:
    print('Usage: {0} <csv_file>'.format(sys.argv[0]))
    exit(1)

csv_file = open(sys.argv[1], 'rt')

try:
    reader = csv.reader(csv_file)
    # Check the indexes of significant fields
    first_row = next(reader)
    st_case_index = first_row.index('ST_CASE')
    persons_index = first_row.index('PERSONS')
    fatals_index = first_row.index('FATALS')
    vehicles_index = first_row.index('VE_TOTAL')
    year_index = first_row.index('YEAR')
    month_index = first_row.index('MONTH')
    day_index = first_row.index('DAY')
    day_of_week_index = first_row.index('DAY_WEEK')
    hour_index = first_row.index('HOUR')
    minute_index = first_row.index('MINUTE')
    latitude_index = first_row.index('LATITUDE')
    longitude_index = first_row.index('LONGITUD')

    accidents = []

    dupa = 0
    for row in reader:
        year = get_int(row, year_index)
        month = get_int(row, month_index)
        day = get_int(row, day_index)
        hour = get_int(row, hour_index)
        if hour > s23:
            dupa += 1
        hour %= 24
        minute = get_int(row, minute_index)
        minute %= 60
        timestamp = 'TIMESTAMP \'{0}-{1}-{2} {3}:{4}:00\''.format(year, month, day, hour, minute)
        new_accident = accident.new(
            # USA ids will be in form 1200700000001234
            # 1 at the beggining means thats from USA
            # 2007 means the year
            # 1234 means the case ID as in FARS data
            id=1000000000000000 + year * 100000000000 + get_int(row, st_case_index),
            country='USA',
            timestamp=timestamp,
            day_of_week=get_int(row, day_of_week_index),
            latitude=get_float(row, latitude_index),
            longitude=get_float(row, longitude_index),
            persons_count=get_int(row, persons_index),
            fatalities_count=get_int(row, fatals_index),
            vehicles_count=get_int(row, vehicles_index),
            speed_limit=-1
        )
        accidents.append(new_accident)
    print(dupa)
    # accident.insert(accidents)

finally:
    csv_file.close()