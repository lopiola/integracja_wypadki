#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Parsing accident CSV files for Great Britain data and putting them into DB
"""

import csv
import sys
import db_api.accident
from parsing.common import get_timestamp, translate_field, to_float, to_int
from parsing.gb_common import get_acc_id

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
    if int(accident_data['Accident_Severity']) == 1:
        return True
    return False


def get_acc_datetime(date, time):
    """
    Builds datetime in a form of dictionary based on date and time
    of accident.
    :param date - Date in format "DD/MM/YYYY"
    :param time - Time in format "HH:mm"
    """
    datetime = {}

    # Date format is "DD/MM/YYYY"
    day = int(date[:2])
    month = int(date[3:5])
    year = int(date[-4:])
    datetime['year'] = year
    datetime['month'] = month
    datetime['day'] = day

    # Time format is "HH:mm"
    hour = int(time[:2])
    minute = int(time[-2:])
    datetime['hour'] = hour
    datetime['minute'] = minute

    return datetime


KILOMETERS_IN_MILE = 1.60934


def mph_to_kmph(mph):
    # TODO: Should it be int?
    return int(mph * KILOMETERS_IN_MILE + 0.5)


"""
A mapping from labels in csv file to a tuple of new label for
database and function for transforming old value into new one.
Transforming functions can have arbitrarily many arguments
that are passed in as kwargs.
"""
translator_map = {
    '\xef\xbb\xbfAccident_Index': ('id', get_acc_id),
    'Longitude': ('longitude', to_float),
    'Latitude': ('latitude', to_float),
    'Date': ('timestamp', get_timestamp),
    # TODO: check day of week codes
    'Day_of_Week': ('day_of_week', to_float),
    'Number_of_Casualties': ('persons_count', to_int),
    'Number_of_Vehicles': ('vehicles_count', to_int),
    'Speed_limit': ('speed_limit', lambda value: mph_to_kmph(int(value)))
}


def get_kwargs(accident_data, field):
    """
    Build kwargs from accident data for a specific field.
    Default is one pair: value = field_value_as_string
    """
    if field == '\xef\xbb\xbfAccident_Index':
        return {'acc_index': accident_data[field]}
    if field == 'Date':
        return get_acc_datetime(accident_data['Date'], accident_data['Time'])
    return {'value': accident_data[field]}

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: {0} <csv_file>'.format(sys.argv[0]))
        exit(1)

    with open(sys.argv[1], 'rt') as csv_file:
        reader = csv.DictReader(csv_file)

        fields = reader.fieldnames
        accidents = []

        for accident_data in reader:
            if is_fatal(accident_data):
                accident = {'country': 'GB'}
                for field in fields:
                    kwargs = get_kwargs(accident_data, field)
                    try:
                        (label, value) = translate_field(field, translator_map, **kwargs)
                        accident[label] = value
                    except ValueError:
                        # We do not want to map this field
                        pass
                # TODO: Get fatalities count. Requires scanning casualties file"
                # (maybe set this to 0 and update when inserting casualties))
                accident['fatalities_count'] = -1
                accidents.append(db_api.accident.new(**accident))
                print(accident)

        db_api.accident.insert(accidents)
