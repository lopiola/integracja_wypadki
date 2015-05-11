#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Common functions for parsers.
"""

"""
Translating dictionary for country codes
"""


def get_gb_acc_id(year, case_index):
    """
    Returns global accident id for GB, year and index of accident.

    GB ids will be in form 2200700000001234
    2 at the beginning means it is from Great Britain
    2007 means the year
    1234 means the case ID as in original data
    """
    try:
        acc_id = 2000000000000000
        acc_id += year * 100000000000
        acc_id += case_index
    except KeyError:
        raise ValueError("Country code incorrect")
    return acc_id


def get_gb_veh_id(acc_id, vehicle_index):
    """
    Returns global vehicle id for GB, year and index of accident.

    The id is constructed as <Acc_id><Vehicle_index>
    where Vehicle_index is two digits max.
    """

    veh_id = acc_id * 100
    veh_id += vehicle_index

    return veh_id


def get_gb_person_id(acc_id, person_index):
    """
    Returns global person id for GB, year and index of accident.

    The id is constructed as <Acc_id><Person_index>
    where Vehicle_index is two digits max.
    """

    person_id = acc_id * 100
    person_id += person_index

    return person_id


def get_usa_acc_id(year, case_index):
    """
    Returns global accident id for USA, year and index of accident.

    USA ids will be in form 1200700000001234
    1 at the beginning means it is from USA
    2007 means the year
    1234 means the case ID as in FARS data
    """
    try:
        acc_id = 1000000000000
        acc_id += year * 10000000
        acc_id += case_index
    except KeyError:
        raise ValueError("Country code incorrect")
    return acc_id


def get_usa_veh_id(acc_id, vehicle_index):
    """
    Returns global vehicle id for USA, year and index of accident.

    The id is constructed as <Acc_id><Vehicle_index>
    where Vehicle_index is three digits max.
    """

    veh_id = acc_id * 1000
    veh_id += vehicle_index

    return veh_id


def get_usa_person_id(acc_id, veh_id, person_index):
    """
    Returns global person id for USA, year and index of accident.

    The id is constructed as <Acc_id><Person_index>
    where Vehicle_index is three digits max.
    """

    person_id = (acc_id * 1000 + veh_id) * 1000
    person_id += person_index

    return person_id


def get_timestamp(year, month, day, hour, minute):
    """
    Formats timestamp from time data.
    """
    hour %= 24
    minute %= 60
    timestamp = 'TIMESTAMP \'{0}-{1}-{2} {3}:{4}:00\''.format(year, month, day, hour, minute)
    return timestamp


def translate_field(label, translator_map, **kwargs):
    """
    Translate field with an old label into a list of tuples of form (new_label, new_value).
    :param translator_map - maps labels to appropriate tuple lists. Supplied by parsing script.
    For each label we get a list of tuples (new_label, mapping_function). Mapping_function invoked
    in the arguments yields the new value.
    :param kwargs - keyword style arguments passed into mapping functions for
    calculating the new values. May be arbitrarily long.
    """
    try:
        new_label_list = []
        label_list = translator_map[label]
        for (new_label, map_function) in label_list:
            new_label_list.append((new_label, map_function(**kwargs)))
    except KeyError:
        raise ValueError("Unknown label")
    return new_label_list


"""
Lambdas for mapping values to simple types.
"""
to_float = lambda value: float(value)
to_int = lambda value: int(value)


def map_from_dictionary(dictionary):
    """
    Returns a function for translating values into new ones based on
    he given mapping dictionary.
    """
    return lambda value: dictionary[value]
