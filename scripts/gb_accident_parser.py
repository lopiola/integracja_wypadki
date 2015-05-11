#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Parsing accident CSV files for Great Britain data and putting them into DB
"""

import csv
import sys
import db_api.accident
from parsing.common import get_timestamp, translate_field, to_float, to_int, map_from_dictionary
from parsing.gb_common import get_acc_id
import cPickle as pickle

# To help remember the names
field_names = [
    '\xef\xbb\xbfAccident_Index',       #done
    'Location_Easting_OSGR',
    'Location_Northing_OSGR',
    'Longitude',                        #done
    'Latitude',                         #done
    'Police_Force',
    'Accident_Severity',                #done
    'Number_of_Vehicles',               #done
    'Number_of_Casualties',             #done
    'Date',                             #done
    'Day_of_Week',
    'Time',                             #done
    'Local_Authority_(District)',
    'Local_Authority_(Highway)',
    '1st_Road_Class',
    '1st_Road_Number',
    'Road_Type',
    'Speed_limit',                      #done
    'Junction_Detail',
    'Junction_Control',
    '2nd_Road_Class',
    '2nd_Road_Number',
    'Pedestrian_Crossing-Human_Control',
    'Pedestrian_Crossing-Physical_Facilities',
    'Light_Conditions',
    'Weather_Conditions',               #done
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
    try:
        hour = int(time[:2])
        minute = int(time[-2:])
        datetime['hour'] = hour
        datetime['minute'] = minute
    except ValueError:
        return None

    return datetime


def get_timestamp_from_date_time(date, time):
    datetime = get_acc_datetime(date, time)
    if not datetime:
        return None
    return get_timestamp(**datetime)

KILOMETERS_IN_MILE = 1.60934

def mph_to_kmph(mph):
    # TODO: Should it be int?
    return int(mph * KILOMETERS_IN_MILE + 0.5)


"""
Mapping dictionaries.
"""
snow_dictionary = {
    '1':    'NO',
    '2':    'NO',
    '3':    'YES',
    '4':    'NO',
    '5':    'NO',
    '6':    'YES',
    '7':    'NO',
    '8':    'NO',
    '-1':   'UNKNOWN',
}

rain_dictionary = {
    '1':    'NO',
    '2':    'YES',
    '3':    'NO',
    '4':    'NO',
    '5':    'YES',
    '6':    'NO',
    '7':    'NO',
    '8':    'NO',
    '-1':   'UNKNOWN',
}

wind_dictionary = {
    '1':    'NO',
    '2':    'NO',
    '3':    'NO',
    '4':    'YES',
    '5':    'YES',
    '6':    'YES',
    '7':    'NO',
    '8':    'NO',
    '-1':   'UNKNOWN',
}

fog_dictionary = {
    '1':    'NO',
    '2':    'NO',
    '3':    'NO',
    '4':    'NO',
    '5':    'NO',
    '6':    'NO',
    '7':    'YES',
    '8':    'NO',
    '-1':   'UNKNOWN',
}


"""
A mapping from labels in csv file to a tuple of new label for
database and function for transforming old value into new one.
Transforming functions can have arbitrarily many arguments
that are passed in as kwargs.
"""
translator_map = {
    '\xef\xbb\xbfAccident_Index': [('id', get_acc_id)],
    'Longitude': [('longitude', to_float)],
    'Latitude': [('latitude', to_float)],
    'Date': [('timestamp', get_timestamp_from_date_time)],
    # TODO: check day of week codes
    'Day_of_Week': [('day_of_week', to_float)],
    'Number_of_Casualties': [('persons_count', to_int)],
    'Number_of_Vehicles': [('vehicles_count', to_int)],
    'Speed_limit': [('speed_limit', lambda value: mph_to_kmph(int(value)))],
    'Weather_Conditions': [
        ('snow', map_from_dictionary(snow_dictionary)),
        ('rain', map_from_dictionary(rain_dictionary)),
        ('fog', map_from_dictionary(fog_dictionary)),
        ('wind', map_from_dictionary(wind_dictionary))
    ]
}


def get_kwargs(accident_data, field):
    """
    Build kwargs from accident data for a specific field.
    Default is one pair: value = field_value_as_string
    """
    if field == '\xef\xbb\xbfAccident_Index':
        return {'acc_index': accident_data[field]}
    if field == 'Date':
        return {'date': accident_data['Date'], 'time': accident_data['Time']}

    return {'value': accident_data[field]}

# TODO: deal with cases where no lat/long given, only osgr
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: {0} <csv_file>'.format(sys.argv[0]))
        exit(1)

    with open(sys.argv[1], 'rt') as csv_file:
        reader = csv.DictReader(csv_file)

        fields = reader.fieldnames
        accidents = []
        new_ids = {}

        for accident_data in reader:
            if is_fatal(accident_data):
                accident = {'country': 'GB'}
                for field in fields:
                    kwargs = get_kwargs(accident_data, field)
                    try:

                        label_list = translate_field(field, translator_map, **kwargs)
                        for (label, value) in label_list:
                            accident[label] = value
                    except ValueError:
                        # We do not want to map this field
                        pass

                if accident['timestamp'] and 'latitude' in accident:
                    accident['fatalities_count'] = 0
                    accidents.append(db_api.accident.new_from_dict(accident))
                # print(accident)

        sorted_accidents = sorted(accidents, key=lambda e: dict.get(e, 'id'))
        for i in xrange(len(sorted_accidents) - 1):
            if sorted_accidents[i]['id'] == sorted_accidents[i + 1]['id']:
                sorted_accidents[i + 1]['id'] += 1000000000000

        for accident in accidents:
            new_ids[accident['id']] = True

        with open("gb_ids.pickle", "wr") as pickle_file:
            try:
                ids = pickle.load(pickle_file)
            except IOError:
                ids = {}
            ids.update(new_ids)
            pickle.dump(ids, pickle_file)

        db_api.accident.insert(accidents)
