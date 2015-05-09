#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Parsing casualties CSV files for Great Britain data and putting them into DB
"""

import sys
import csv
import db_api.person
import db_api.accident
from parsing import common
from parsing.common import translate_field, map_from_dictionary
from parsing.gb_common import get_acc_id, check_acc_id_for_data, get_veh_id, \
    get_acc_id_from_data, random_from_age_band


# To remember the names

fields = [
    '\xef\xbb\xbfAcc_Index',    #done
    'Vehicle_Reference',        #done
    'Casualty_Reference',       #done
    'Casualty_Class',
    'Sex_of_Casualty',          #done
    'Age_Band_of_Casualty',     #done
    'Casualty_Severity',        #done
    'Pedestrian_Location',
    'Pedestrian_Movement',
    'Car_Passenger',
    'Bus_or_Coach_Passenger',
    'Pedestrian_Road_Maintenance_Worker',
    'Casualty_Type',
    'Casualty_Home_Area_Type'
]


def get_person_id(person_data):
    """
    Mapping function for person id.
    """
    person_ref = person_data['Casualty_Reference']
    acc_id = get_acc_id_from_data(person_data)
    person_id = common.get_person_id(acc_id, int(person_ref))
    return person_id


"""
Mapping dictionaries.
"""
casualty_sex_dictionary = {
    '1':    'MALE',
    '2':    'FEMALE',
    '-1':   'UNKNOWN',
}

casualty_severity_dictionary = {
    '1':    'FATAL',
    '2':    'SERIOUS',
    '3':    'SLIGHT',
}

car_passenger_dictionary = {
    '0':    'NONE',
    # TODO: differentiate between driver and passenger, 1 means front
    '1':    'PASSENGER',
    '2':    'BACK',
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
    'Vehicle_Reference': [('veh_id', get_veh_id)],
    'Casualty_Reference': [('id', get_person_id)],
    'Sex_of_Casualty': [('sex', map_from_dictionary(casualty_sex_dictionary))],
    'Casualty_Severity': [('injury_level', map_from_dictionary(casualty_severity_dictionary))],
    'Car_Passenger': [('seated_pos', map_from_dictionary(car_passenger_dictionary))],
    'Age_Band_of_Casualty': [('age', random_from_age_band)],
}


def get_kwargs(person_data, field):
    """
    Build kwargs from accident data for a specific field.
    Default is one pair: value = field_value_as_string
    """
    if field == '\xef\xbb\xbfAcc_Index':
        return {'acc_index': person_data[field]}
    if field == 'Vehicle_Reference':
        return {'gb_data': person_data}
    if field == 'Casualty_Reference':
        return {'person_data': person_data}
    return {'value': person_data[field]}


def update_fatalities_counts(persons):
    """
    Increases fatalities counts for fatal victims on the persons list.
    """
    for person in persons:
        if person['injury_level'] == 'FATAL':
            acc_id = person['acc_id']
            db_api.accident.increase_value(acc_id, 'fatalities_count')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: {0} <csv_file>'.format(sys.argv[0]))
        exit(1)

    with open(sys.argv[1], 'rt') as csv_file:
        reader = csv.DictReader(csv_file)

        fields = reader.fieldnames
        persons = []

        for person_data in reader:
            person = {}
            if check_acc_id_for_data(person_data):
                for field in fields:
                    kwargs = get_kwargs(person_data, field)
                    try:
                        label_list = translate_field(field, translator_map, **kwargs)
                        for (label, value) in label_list:
                            person[label] = value
                    except ValueError:
                        # We do not want to map this field
                        pass
                persons.append(db_api.person.new_from_dict(person))
                print(person)

        # db_api.person.insert(persons)
        update_fatalities_counts(persons)
