#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module handles mapping of rows from FARS data into common format.

Significant attributes:
ST_CASE - case ID
VEH_NO - vehicle
NUMOCCS - number of occupants
"""

import csv
import sys
from db_api import vehicle


def get_int(list_row, index):
    return int(float(list_row[index]))


def get_float(list_row, index):
    return float(list_row[index])


if len(sys.argv) != 3:
    print('Usage: {0} <csv_file> <year>'.format(sys.argv[0]))
    exit(1)

csv_file = open(sys.argv[1], 'rt')
year = int(sys.argv[2])

try:
    reader = csv.reader(csv_file)
    # Check the indexes of significant fields
    first_row = next(reader)
    st_case_index = first_row.index('ST_CASE')
    veh_no_index = first_row.index('VEH_NO')
    num_occs_index = first_row.index('NUMOCCS')

    vehicles = []

    for row in reader:
        new_vehicle = vehicle.new(
            # USA ids will be in form 1200700000001234
            # 1 at the beggining means that it is from USA
            # 2007 means the year
            # 1234 means the case ID as in FARS data
            id=10000 * get_int(row, st_case_index) + get_int(row, veh_no_index),
            acc_id=1000000000000000 + year * 100000000000 + get_int(row, st_case_index),
            driver_age=-1,
            driver_sex='UNKNOWN',
            passenger_count= get_int(row, num_occs_index)
        )
        vehicles.append(new_vehicle)
    vehicle.insert(vehicles)

finally:
    csv_file.close()