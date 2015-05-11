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
    '1':    'MALE',
    '2':    'FEMALE',
    '3':    'UNKNOWN',
    '-1':   'UNKNOWN',
}

skidding_dictionary = {
    '0':    'NO',
    '1':    'YES',
    '2':    'YES',
    '3':    'NO',
    '4':    'NO',
    '5':    'NO',
    '-1':   'UNKNOWN',
}

rollover_dictionary = {
    '0':    'NO',
    '1':    'NO',
    '2':    'YES',
    '3':    'NO',
    '4':    'YES',
    '5':    'YES',
    '-1':   'UNKNOWN',
}

jackknifing_dictionary = {
    '0':    'NO',
    '1':    'NO',
    '2':    'NO',
    '3':    'YES',
    '4':    'YES',
    '5':    'NO',
    '-1':   'UNKNOWN',
}

type_dictionary = {
    '1':    'OTHER',
    '2':    'MOTORCYCLE',
    '3':    'MOTORCYCLE',
    '4':    'MOTORCYCLE',
    '5':    'MOTORCYCLE',
    '8':    'CAR',
    '9':    'CAR',
    '10':   'BUS',
    '11':   'BUS',
    '16':   'OTHER',
    '17':   'AGRICULTURAL',
    '18':   'OTHER',
    '19':   'CARGO',
    '20':   'CARGO',
    '21':   'CARGO',
    '22':   'OTHER',
    '23':   'MOTORCYCLE',
    '90':   'OTHER',
    '97':   'MOTORCYCLE',
    '98':   'CARGO',
    '103':   'MOTORCYCLE',
    '104':   'MOTORCYCLE',
    '105':   'MOTORCYCLE',
    '106':   'MOTORCYCLE',
    '108':   'CAR',
    '109':   'CAR',
    '110':   'BUS',
    '113':   'CARGO',
    '-1':   'UNKNOWN',
}

maneuver_dictionary = {
    '1':    'REVERSING',
    '2':    'PARKED',
    '3':    'HELD_UP',
    '4':    'STOPPING',
    '5':    'STARTING',
    '6':    'U_TURN',
    '7':    'LEFT',
    '8':    'HELD_UP',
    '9':    'RIGHT',
    '10':   'HELD_UP',
    '11':   'CHANGING_LANE',
    '12':   'CHANGING_LANE',
    '13':   'OVERTAKING',
    '14':   'OVERTAKING',
    '15':   'OVERTAKING',
    '16':   'CURVING',
    '17':   'CURVING',
    '18':   'STRAIGHT',
    '-1':   'UNKNOWN',

}

fuel_type_dictionary = {
    '1':    'PETROL',
    '2':    'OTHER',
    '3':    'OTHER',
    '4':    'OTHER',
    '5':    'GAS',
    '6':    'GAS',
    '7':    'GAS',
    '8':    'HYBRID',
    '9':    'OTHER',
    '10':   'OTHER',
    '-1':   'UNKNOWN',

}
# TODO: Wouldn't OFFSIDE and NEARSIDE be better after all?
impact_area_dictionary = {
    '0':    'NON_COLLISION',
    '1':    'FRONT',
    '2':    'BACK',
    '3':    'LEFT_SIDE',
    '4':    'RIGHT_SIDE',
    '-1':   'UNKNOWN',
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
    'Sex_of_Driver': [('driver_sex', map_from_dictionary(driver_sex_dictionary))],
    'Skidding_and_Overturning':
        [('skidded', map_from_dictionary(skidding_dictionary)),
         ('rollover', map_from_dictionary(rollover_dictionary)),
         ('jackknifing', map_from_dictionary(jackknifing_dictionary))
         ],
    'Age_Band_of_Driver': [('driver_age', random_from_age_band)],
    'Vehicle_Type': [('type', map_from_dictionary(type_dictionary))],
    '1st_Point_of_Impact': [('first_impact_area', map_from_dictionary(impact_area_dictionary))],
    'Propulsion_Code': [('fuel_type', map_from_dictionary(fuel_type_dictionary))],
    'Vehicle_Manoeuvre': [('maneuver', map_from_dictionary(maneuver_dictionary))],
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

        db_api.vehicle.insert(vehicles)