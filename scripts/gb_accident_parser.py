#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Parsing accident CSV files for Great Britain data and putting them into DB
"""

import csv
import sys
import db_api.accident
from parsing.common import get_timestamp, translate_field, to_float, to_int, map_from_dictionary
from parsing.gb_common import get_acc_id, GB_IDS_FILE, get_gb_ids
import cPickle as pickle


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

road_class_dictionary = {
    '1':    'MOTORWAY',
    '2':    'MOTORWAY',
    '3':    'PRINCIPAL',
    '4':    'MAJOR',
    '5':    'MINOR',
    '6':    'UNCLASSIFIED',
    '-1':   'UNKNOWN',
}

junction_dictionary = {
    '0':    'NON_JUNCTION',
    '1':    'INTERSECTION',
    '2':    'INTERSECTION',
    '3':    'INTERSECTION',
    '4':    'INTERSECTION',
    '5':    'RAMP',
    '6':    'INTERSECTION',
    '7':    'INTERSECTION',
    '8':    'DRIVEWAY',
    '9':    'INTERSECTION',
    '-1':    'UNKNOWN',
}

surface_dictionary = {
    '1':    'DRY',
    '2':    'WET',
    '3':    'SNOW',
    '4':    'ICE',
    '5':    'FLOOD',
    '6':    'OTHER',
    '7':    'OTHER',
    '-1':    'UNKNOWN',
}

lighting_dictionary = {
    '1':    'DAYLIGHT',
    '4':    'DARK_LIGHTED',
    '5':    'DARK',
    '6':    'DARK',
    '7':    'DARK',
    '-1':   'UNKNOWN',
}

junction_control_dictionary = {
    '0':    'YIELD_OR_NONE',
    '1':    'AUTH_PERSON',
    '2':    'TRAFFIC_SIGNAL',
    '3':    'STOP_SIGN',
    '4':    'YIELD_OR_NONE',
    '-1':   'UNKNOWN',
}


def is_signal_malfunction(special_conditions):
    return special_conditions in ['1', '2']


def map_junction_control(junction_control, special_conditions):
    if is_signal_malfunction(special_conditions):
        return 'SIGNAL_MALF'
    else:
        return junction_control_dictionary[junction_control]
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
    'Day_of_Week': [('day_of_week', to_float)],
    'Number_of_Casualties': [('persons_count', to_int)],
    'Number_of_Vehicles': [('vehicles_count', to_int)],
    'Speed_limit': [('speed_limit', lambda value: mph_to_kmph(int(value)))],
    'Weather_Conditions': [
        ('snow', map_from_dictionary(snow_dictionary)),
        ('rain', map_from_dictionary(rain_dictionary)),
        ('fog', map_from_dictionary(fog_dictionary)),
        ('wind', map_from_dictionary(wind_dictionary))
    ],
    '1st_Road_Class': [('road_class', map_from_dictionary(road_class_dictionary))],
    'Junction_Detail': [('relation_to_junction', map_from_dictionary(junction_dictionary))],
    'Road_Surface_Conditions': [('surface_cond', map_from_dictionary(surface_dictionary))],
    'Light_Conditions': [('lighting', map_from_dictionary(lighting_dictionary))],
    'Junction_Control': [('traffic_control', map_junction_control)]
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
    if field == 'Junction_Control':
        return {'junction_control': accident_data[field], 'special_conditions': accident_data['Special_Conditions_at_Site']}
    return {'value': accident_data[field]}


def update_ids(accidents):
    new_ids = {}
    for accident in accidents:
        new_ids[accident['id']] = True

    ids = get_gb_ids()
    ids.update(new_ids)

    with open(GB_IDS_FILE, "w+") as pickle_file:
        pickle.dump(ids, pickle_file)


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

                        label_list = translate_field(field, translator_map, **kwargs)
                        for (label, value) in label_list:
                            accident[label] = value
                    except ValueError:
                        # We do not want to map this field
                        pass

                # TODO: Change this and cound lat/long from osgr
                # For now setting to incorrect value (lat/long) can't be more than 180
                if 'latitude' not in accident:
                    accident['latitude'] = 200.0
                    accident['longitude'] = 200.0

                if accident['timestamp']:
                    accident['fatalities_count'] = 0
                    accidents.append(db_api.accident.new_from_dict(accident))

                    print accident

        db_api.accident.insert(accidents)
        update_ids(accidents)

