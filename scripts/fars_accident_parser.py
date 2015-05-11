#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Parsing FARS vehicle CSV files and putting them into DB

"""

import csv
import sys
from db_api import accident
from fars_accident_mapper import FARSAccidentMapper


if len(sys.argv) != 2:
    print('Usage: {0} <csv_file>'.format(sys.argv[0]))
    exit(1)

csv_file = open(sys.argv[1], 'rt')

try:
    reader = csv.reader(csv_file)
    first_row = next(reader)
    mapper = FARSAccidentMapper(first_row)

    accidents = []
    for row in reader:
        if mapper.valid(row):
            new_accident = accident.new(
                id=mapper.id(row),
                country='USA',
                timestamp=mapper.timestamp(row),
                day_of_week=mapper.day_of_week(row),
                latitude=mapper.latitude(row),
                longitude=mapper.longitude(row),
                persons_count=mapper.persons_count(row),
                fatalities_count=mapper.fatalities_count(row),
                vehicles_count=mapper.vehicles_count(row),
                speed_limit=mapper.speed_limit(row),
                snow=mapper.snow(row),
                rain=mapper.rain(row),
                wind=mapper.wind(row),
                fog=mapper.fog(row),
                relation_to_junction=mapper.relation_to_junction(row),
                road_class=mapper.road_class(row),
                surface_cond=mapper.surface_cond(row),
                lighting=mapper.lighting(row),
                traffic_control=mapper.traffic_control(row),
                other_conditions=mapper.other_conditions(row)
            )
            accidents.append(new_accident)
    accident.insert(accidents)

finally:
    csv_file.close()