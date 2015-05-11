#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import common
import cPickle as pickle
import hashlib

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


def index_letter_to_integer(index_letter):
    """
    Turns letters from accident index into a distinct integer.
    """
    return ord(index_letter)


def get_acc_year(acc_index):
    """
    Returns the year extracted from accident index
    """
    return int(acc_index[0:4])


def get_case_index(acc_index):
    case_index = 0
    for char in acc_index[5:]:
        char_value = ord(char)
        int_value = char_value - ord('0')
        if 10 > int_value >= 0:
            char_value = int_value
        else:
            char_value = char_value - ord('A') + 10
        multi = 36
        case_index += char_value
        case_index *= multi
    case_index /= 36
    # print case_index
    return case_index


# def get_case_index(acc_index):
#     # m = hashlib.md5()
#     # m.update(acc_index[5:])
#     # case_index = int(m.hexdigest(), 16)
#     case_index = hash(acc_index[5:])
#     print acc_index[5:]
#     print case_index
#     return case_index


def get_acc_id(acc_index):
    """
    Returns global accident id based on accident index as in Great Britain original data.
    """
    year = get_acc_year(acc_index)
    case_index = get_case_index(acc_index)

    return get_gb_acc_id(year, case_index)


ids = None


def check_acc_id_for_data(gb_data):
    """
    Checks if accident id for this vehicle is in database.
    Ensures that we insert data about vehicles that took part in fatal crashes only.
    """
    global ids
    acc_id = get_acc_id_from_data(gb_data)
    if not ids:
        with open("gb_ids.pickle") as pickle_file:
            ids = pickle.load(pickle_file)
    return acc_id in ids
    # return db_api.accident.select(acc_id) is not None


def get_veh_id(gb_data):
    """
    Mapping function for vehicle id
    """
    veh_ref = gb_data['Vehicle_Reference']
    acc_id = get_acc_id_from_data(gb_data)
    veh_id = common.get_gb_veh_id(acc_id, int(veh_ref))
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