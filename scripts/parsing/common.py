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
    Get id for usa cases.
    """
    return get_acc_id(year, case_index, 'USA')


def get_gb_acc_id(year, case_index):
    """
    Get id for Great Britain cases
    """
    return get_acc_id(year, case_index, 'GB')


def get_acc_id(year, case_index, country):
    """
    Get global accident id according to country, year and index of accident.

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


def get_timestamp(year, month, day, hour, minute):
    hour %= 24
    minute %= 60
    timestamp = 'TIMESTAMP \'{0}-{1}-{2} {3}:{4}:00\''.format(year, month, day, hour, minute)
    return timestamp