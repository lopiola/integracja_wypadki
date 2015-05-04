#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Parsing vehicle CSV files for Great Britain data and putting them into DB
"""

import sys
import csv
import db_api.vehicle
import db_api.accident
from gb_accident_parser import get_acc_id, get_acc_year
from parsing import common

# To help remember the names
field_names = [
    '\xef\xbb\xbfAcc_Index',
    'Vehicle_Reference',
    'Vehicle_Type',
    'Towing_and_Articulation',
    'Vehicle_Manoeuvre',
    'Vehicle_Location-Restricted_Lane',
    'Junction_Location',
    'Skidding_and_Overturning',
    'Hit_Object_in_Carriageway',
    'Vehicle_Leaving_Carriageway',
    'Hit_Object_off_Carriageway',
    '1st_Point_of_Impact',
    'Was_Vehicle_Left_Hand_Drive?',
    'Journey_Purpose_of_Driver',
    'Sex_of_Driver',
    'Age_Band_of_Driver',
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
        acc_index = vehicle_data[field]
        return {'year': get_acc_year(acc_index), 'acc_index': acc_index}
    if field == 'Vehicle_Reference':
        return {'vehicle_data': vehicle_data, 'veh_ref': vehicle_data[field]}
    return {'value': vehicle_data[field]}


def get_veh_id(vehicle_data, veh_ref):
    """
    Mapping function for vehicle id
    """
    veh_id = common.get_veh_id(
        get_acc_id_from_vehicle_data(vehicle_data),
        int(veh_ref)
    )
    return veh_id


"""
A mapping from labels in csv file to a tuple of new label for
database and function for transforming old value into new one.
Transforming functions can have arbitrarily many arguments
that are passed in as kwargs.
"""
translator_map = {
    '\xef\xbb\xbfAcc_Index': ('acc_id', get_acc_id),
    'Vehicle_Reference' : ('id', get_veh_id),
    'Age_Band_of_Driver': ('driver_age', lambda value: 0),
    'Sex_of_Driver': ('driver_sex', lambda value: 'UNKNOWN')
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


def get_acc_id_from_vehicle_data(vehicle_data):
    """
    Based on vehicle data constructs accident id.
    """
    label = '\xef\xbb\xbfAcc_Index'
    _, acc_id = translate_field(label, **get_kwargs(vehicle_data, label))
    return acc_id


def check_acc_id(vehicle_data):
    """
    Checks if accident id for this vehicle is in database.
    Ensures that we insert data about vehicles that took part in fatal crashes only.
    """
    acc_id = get_acc_id_from_vehicle_data(vehicle_data)
    return db_api.accident.select(acc_id) is not None


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: {0} <csv_file>'.format(sys.argv[0]))
        exit(1)

    with open(sys.argv[1], 'rt') as csv_file:
        reader = csv.DictReader(csv_file)

        fatal = 0
        non_fatal = 0

        fields = reader.fieldnames
        vehicles = []

        for vehicle_data in reader:
            vehicle = {}
            if check_acc_id(vehicle_data):
                for field in fields:
                    if field == 'Vehicle_Reference':
                        print vehicle_data[field]
                    kwargs = get_kwargs(vehicle_data, field)
                    try:
                        (label, value) = translate_field(field, **kwargs)
                        vehicle[label] = value
                    except ValueError:
                        pass
                # TODO: count this based on casualties file
                vehicle['passenger_count'] = 0
                vehicles.append(db_api.vehicle.new(**vehicle))
                print(vehicle)

        # db_api.vehicle.insert(vehicles)