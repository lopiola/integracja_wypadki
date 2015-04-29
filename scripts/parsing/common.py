#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Common functions for parsers.
"""

country_code = {
    'usa': 1,
    'gb': 2
}


def get_usa_acc_id (year, case_index):
    return get_acc_id(year, case_index, 'usa')


def get_gb_acc_id(year, case_index):
    return get_acc_id(year, case_index, 'gb')


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
        acc_id = country_code[country] * 1e15
        acc_id += year * 1e11
        acc_id += case_index
    except KeyError:
        raise ValueError("Country code incorrect")
    return acc_id

