#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Parsing accident CSV files for Great Britain data and putting them into DB
"""

import csv
import sys
import parsing.common
from db_api import accident


# To help remember the names
field_names = [
    '\xef\xbb\xbfAccident_Index',
    'Location_Easting_OSGR',
    'Location_Northing_OSGR',
    'Longitude',
    'Latitude',
    'Police_Force',
    'Accident_Severity',
    'Number_of_Vehicles',
    'Number_of_Casualties',
    'Date',
    'Day_of_Week',
    'Time',
    'Local_Authority_(District)',
    'Local_Authority_(Highway)',
    '1st_Road_Class',
    '1st_Road_Number',
    'Road_Type',
    'Speed_limit',
    'Junction_Detail',
    'Junction_Control',
    '2nd_Road_Class',
    '2nd_Road_Number',
    'Pedestrian_Crossing-Human_Control',
    'Pedestrian_Crossing-Physical_Facilities',
    'Light_Conditions',
    'Weather_Conditions',
    'Road_Surface_Conditions',
    'Special_Conditions_at_Site',
    'Carriageway_Hazards',
    'Urban_or_Rural_Area',
    'Did_Police_Officer_Attend_Scene_of_Accident',
    'LSOA_of_Accident_Location'
]


def is_fatal(accident_data):
    if get_int(accident_data, 'Accident_Severity') == 1:
        return True
    return False


# TODO: move to common
def get_int(list_row, index):
    return int(float(list_row[index]))


def get_id(year, acc_index):
    """
    Mapping function for id.
    """
    case_index = int(acc_index[-5:])
    return parsing.common.get_gb_acc_id(year, case_index)


"""
A mapping from labels in csv file to a tuple of new label for
datatabase and function for transforming old value into new one.
Transforming functions can have arbitrarily many arguments
that are passed in as kwargs.
"""
translator_map = {
    '\xef\xbb\xbfAccident_Index': ('id', get_id),
    'Longitude': ('longitude', lambda value: float(value)),
    'Latitude': ('latitude', lambda value: float(value))
}


def translate_field(label, **kwargs):
    """
    Translate field with an old label into tuple (new_label, new_value).
    :param kwargs - keyword style arguments passed into mapping function to
        calculate the new value. May be arbitrarily big.
    """
    try:
        (new_label, map_function) = translator_map[label]
        return new_label, map_function(**kwargs)
    except KeyError:
        raise ValueError("Unknown label")


def get_kwargs(accident_data, field):
    """
    Build kwargs from accident data for a specific field.
    Default is one pair value = field_value_as_string
    """
    if field == '\xef\xbb\xbfAccident_Index':
        return {'year': 2000, 'acc_index': accident_data['\xef\xbb\xbfAccident_Index']}
    return {'value': accident_data[field]}


if len(sys.argv) != 2:
    print('Usage: {0} <csv_file>'.format(sys.argv[0]))
    exit(1)

with open(sys.argv[1], 'rt') as csv_file:
    reader = csv.DictReader(csv_file)

    fatal = 0
    non_fatal = 0

    fields = reader.fieldnames

    for accident_data in reader:
        if is_fatal(accident_data):
            accident = {}
            for field in fields:
                kwargs = get_kwargs(accident_data, field)
                try:
                    (label, value) = translate_field(field, **kwargs)
                    accident[label] = value
                except ValueError:
                    pass
                    # print('Ignoring field with label {0}'.format(field))
            # print accident
            fatal += 1
        else:
            non_fatal += 1
    print(fatal, non_fatal)
