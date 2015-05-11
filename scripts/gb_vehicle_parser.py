#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Parsing vehicle CSV files for Great Britain data and putting them into DB
"""

import sys
import csv
import db_api.vehicle
import db_api.accident
from parsing.common import translate_field, map_from_dictionary
from parsing.gb_common import get_acc_id, check_acc_id_for_data, get_veh_id, random_from_age_band

field_names = [
    '\xef\xbb\xbfAcc_Index',            #done
    'Vehicle_Reference',                #done
    'Vehicle_Type',
    'Towing_and_Articulation',
    'Vehicle_Manoeuvre',
    'Vehicle_Location-Restricted_Lane',
    'Junction_Location',
    'Skidding_and_Overturning',         #done
    'Hit_Object_in_Carriageway',
    'Vehicle_Leaving_Carriageway',
    'Hit_Object_off_Carriageway',
    '1st_Point_of_Impact',
    'Was_Vehicle_Left_Hand_Drive?',
    'Journey_Purpose_of_Driver',
    'Sex_of_Driver',                    #done
    'Age_Band_of_Driver',               #done
    'Engine_Capacity_(CC)',
    'Propulsion_Code',
    'Age_of_Vehicle',
    'Driver_IMD_Decile',
    'Driver_Home_Area_Type'
]


def get_kwargs(vehicle_data, field):
    """
    Build kwargs from accident data for a specific field.
    Default is one pair value = field_value_as_string
    """
    if field == '\xef\xbb\xbfAcc_Index':
        return {'acc_index': vehicle_data[field]}
    if field == 'Vehicle_Reference':
        return {'gb_data': vehicle_data}
    return {'value': vehicle_data[field]}


"""
Mapping dictionaries.
"""
driver_sex_dictionary = {
    '1': 'MALE',
    '2': 'FEMALE',
    '3': 'UNKNOWN',
    '-1': 'UNKNOWN',
}

skidding_dictionary = {
    '0': 'NO',
    '1': 'YES',
    '2': 'YES',
    '3': 'NO',
    '4': 'NO',
    '5': 'NO',
    '-1': 'UNKNOWN',
}

rollover_dictionary = {
    '0': 'NO',
    '1': 'NO',
    '2': 'YES',
    '3': 'NO',
    '4': 'YES',
    '5': 'YES',
    '-1': 'UNKNOWN',
}

jackknifing_dictionary = {
    '0': 'NO',
    '1': 'NO',
    '2': 'NO',
    '3': 'YES',
    '4': 'YES',
    '5': 'NO',
    '-1': 'UNKNOWN',
}

"""
A mapping from labels in csv file to a tuple of new label for
database and function for transforming old value into new one.
Transforming functions can have arbitrarily many arguments
that are passed in as kwargs.
"""
translator_map = {
    '\xef\xbb\xbfAcc_Index': [('acc_id', get_acc_id)],
    'Vehicle_Reference': [('id', get_veh_id)],
    'Age_Band_of_Driver': [('driver_age', lambda value: 0)],
    'Sex_of_Driver': [('driver_sex', map_from_dictionary(driver_sex_dictionary))],
    'Skidding_and_Overturning':
        [('skidded', map_from_dictionary(skidding_dictionary)),
         ('rollover', map_from_dictionary(rollover_dictionary)),
         ('jackknifing', map_from_dictionary(jackknifing_dictionary))
         ],
    'Age_Band_of_Driver': [('driver_age', random_from_age_band)],
}

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: {0} <csv_file>'.format(sys.argv[0]))
        exit(1)

    with open(sys.argv[1], 'rt') as csv_file:
        reader = csv.DictReader(csv_file)

        fields = reader.fieldnames
        vehicles = []

        for vehicle_data in reader:
            vehicle = {}
            if check_acc_id_for_data(vehicle_data):
                for field in fields:
                    kwargs = get_kwargs(vehicle_data, field)
                    try:
                        label_list = translate_field(field, translator_map, **kwargs)
                        for (label, value) in label_list:
                            vehicle[label] = value
                    except ValueError:
                        # We do not want to map this field
                        pass
                vehicle['passenger_count'] = 0
                print(vehicle)
                vehicles.append(db_api.vehicle.new_from_dict(vehicle))
            else:
                print vehicle_data['\xef\xbb\xbfAcc_Index']

        db_api.vehicle.insert(vehicles)