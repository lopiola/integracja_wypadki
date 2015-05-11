#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Parsing FARS vehicle CSV files and putting them into DB

"""

import csv
import sys
from db_api import person
from fars_person_mapper import FARSPersonMapper


if len(sys.argv) != 3:
    print('Usage: {0} <csv_file> <year>'.format(sys.argv[0]))
    exit(1)

csv_file = open(sys.argv[1], 'rt')
year = int(sys.argv[2])

try:
    reader = csv.reader(csv_file)
    first_row = next(reader)
    mapper = FARSPersonMapper(first_row, year)
    persons = []
    for row in reader:
        if mapper.valid(row):
            print(mapper.id(row))
            TODO COS NIE TAK Z ID!!!S
            new_person = person.new(
                id=mapper.id(row),
                acc_id=mapper.acc_id(row),
                veh_id=mapper.veh_id(row),
                sex=mapper.sex(row),
                age=mapper.age(row),
                injury_level=mapper.injury_level(row),
                type=mapper.type(row),
                seatbelt=mapper.seatbelt(row),
                seated_pos=mapper.seated_pos(row)
            )
            persons.append(new_person)
    person.insert(persons)

finally:
    csv_file.close()