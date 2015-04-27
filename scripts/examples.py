#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Examples of how to use scripts in this directory
"""

from db_api import accident

accident1 = accident.new(
    id=11,
    timestamp='TIMESTAMP \'2014-05-16 15:36:38\'',
    day_of_week=7,
    latitude=23.3453451,
    longtitude=56.23424234,
    persons_count=3,
    fatalities_count=2,
    vehicles_count=1,
    speed_limit=-1,
    surface_cond='SDFG'
)

# accident1 = {
# 'id': 11,
# 'timestamp': 'TIMESTAMP \'2014-05-16 15:36:38\'',
#     'day_of_week': 7,
#     'latitude': 23.3453451,
#     'longtitude': 56.23424234,
#     'persons_count': 3,
#     'fatalities_count': 2,
#     'vehicles_count': 1,
#     'speed_limit': 70
# }
#
# accident2 = {
#     'id': 14,
#     'timestamp': 'TIMESTAMP \'2014-05-17 12:11:10\'',
#     'day_of_week': 7,
#     'latitude': 23.3453451,
#     'longtitude': 56.23424234,
#     'persons_count': 3,
#     'fatalities_count': 2,
#     'vehicles_count': 1,
#     'speed_limit': 70
# }
#
# accident.add([accident1, accident2])