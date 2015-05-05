#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Common functions for parsers.
"""

"""
Translating dictionary for country codes
"""
country_code = {
    'USA': 1,
    'GB': 2
}


def get_usa_acc_id(year, case_index):
    """
    Returns id for usa cases.
    """
    return get_acc_id(year, case_index, 'USA')


def get_gb_acc_id(year, case_index):
    """
    Returns id for Great Britain cases
    """
    return get_acc_id(year, case_index, 'GB')


def get_acc_id(year, case_index, country):
    """
    Returns global accident id according to country, year and index of accident.

    USA ids will be in form 1200700000001234
    1 at the beginning means it is from USA
    2007 means the year
    1234 means the case ID as in FARS data

    GB ids will be in form 2200700000001234
    2 at the beginning means it is from Great Britain
    2007 means the year
    1234 means the case ID as in original data
    """
    try:
        acc_id = country_code[country] * 1000000000000000
        acc_id += year * 100000000000
        acc_id += case_index
    except KeyError:
        raise ValueError("Country code incorrect")
    return acc_id


def get_veh_id(acc_id, vehicle_index):
    """
    Returns global vehicle id according to country, year and index of accident.

    The id is constructed as <Acc_id><Vehicle_index>
    where Vehicle_index is two digits max.
    """

    veh_id = acc_id * 100
    veh_id += vehicle_index

    return veh_id


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
    Translate field with an old label into tuple (new_label, new_value).
    :param translator_map - maps labels to appropriate tuples. Supplied by parsing script.
    :param kwargs - keyword style arguments passed into mapping function to
        calculate the new value. May be arbitrarily big.
    """
    try:
        (new_label, map_function) = translator_map[label]
        return new_label, map_function(**kwargs)
    except KeyError:
        raise ValueError("Unknown label")


"""
Lambdas for mapping values to simple types.
"""
to_float = lambda value: float(value)
to_int = lambda value: int(value)
