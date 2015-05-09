#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import db_api.accident
import common

"""
Common functions for parsers of data from Great Britain.
"""

from common import get_gb_acc_id


def get_acc_id_from_data(gb_data):
    """
    Extracts accident index from Great Britain Data and converts it to global accident id.
    """
    label = '\xef\xbb\xbfAccident_Index'
    if label not in gb_data:
        label = '\xef\xbb\xbfAcc_Index'

    if label not in gb_data:
        raise ValueError('Improper gb_data, no accident index label')

    acc_index = gb_data[label]

    return get_acc_id(acc_index)


def index_letters_to_integer(index_letters):
    """
    Turns letters from accident index into a distinct integer.
    """
    return ord(index_letters[0]) * 128 + ord(index_letters[1])


def get_acc_year(acc_index):
    """
    Returns the year extracted from accident index
    """
    return int(acc_index[0:4])


def get_acc_id(acc_index):
    """
    Returns global accident id based on accident index as in Great Britain original data.
    """
    year = get_acc_year(acc_index)
    case_index = index_letters_to_integer(acc_index[-7:-5]) * 100000
    case_index += int(acc_index[-5:])
    return get_gb_acc_id(year, case_index)


def check_acc_id_for_data(gb_data):
    """
    Checks if accident id for this vehicle is in database.
    Ensures that we insert data about vehicles that took part in fatal crashes only.
    """
    acc_id = get_acc_id_from_data(gb_data)
    return db_api.accident.select(acc_id) is not None


def get_veh_id(gb_data):
    """
    Mapping function for vehicle id
    """
    veh_ref = gb_data['Vehicle_Reference']
    acc_id = get_acc_id_from_data(gb_data)
    veh_id = common.get_veh_id(acc_id, int(veh_ref))
    return veh_id


def random_from_age_band(value):
    """
    Returns a random age value form age band specified in value parameter.
    :param value - age band label as in gb data.
    """
    (begin, end) = age_band_dictionary[value]
    return random.randint(begin, end)


"""
Mapping from age band labels to age band boundaries
"""
age_band_dictionary = {
    '-1':    (-1, -1),
    '1':     (0, 5),
    '2':     (6, 10),
    '3':     (11, 15),
    '4':     (16, 20),
    '5':     (21, 25),
    '6':     (26, 35),
    '7':     (36, 45),
    '8':     (46, 55),
    '9':     (56, 65),
    '10':    (66, 75),
    '11':    (75, 90),
}