#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Examples of how to use scripts in this directory
"""

from db_api import accident

accident1_id = 11
accident1 = accident.new(
    id=accident1_id,
    country='USA',
    timestamp='TIMESTAMP \'2014-05-16 15:36:38\'',
    day_of_week=7,
    latitude=23.3453451,
    longitude=56.23424234,
    persons_count=3,
    fatalities_count=2,
    vehicles_count=1,
    speed_limit=-1
)

accident.insert(accident1)
accident.delete(accident1_id)
accident.insert(accident1)
