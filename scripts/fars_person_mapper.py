#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module handles mapping of rows from FARS data into common format.

Significant attributes:
ST_CASE - case ID
VEH_NO - vehicle number
PER_NO - person number
AGE
PER_TYP
INJ_SEV
SEAT_POS
REST_USE - restraint system use
"""

from parsing import fars_common
from parsing import common


class FARSPersonMapper:
    def __init__(self, first_row, year):
        self.first_row = first_row
        self.year = year
        # Check the indexes of significant fields
        self.st_case_index = self.index_of('ST_CASE')
        self.vehicle_no_index = self.index_of('VEH_NO')
        self.person_no_index = self.index_of('PER_NO')
        self.age_index = self.index_of('AGE')
        self.sex_index = self.index_of('SEX')
        self.type_index = self.index_of('PER_TYP')
        self.injury_index = self.index_of('INJ_SEV')
        self.seated_pos_index = self.index_of('SEAT_POS')
        self.seatbelt_index = self.index_of('REST_USE')

    def valid(self, csv_row):
        return True

    def index_of(self, key):
        index = -1
        try:
            index = self.first_row.index(key)
        except ValueError:
            print('WARNING: Cannot find index of {0}'.format(key))
            pass
        return index

    def acc_id(self, csv_row):
        return common.get_usa_acc_id(self.year, get_int(csv_row, self.st_case_index))

    def veh_id(self, csv_row):
        return common.get_usa_veh_id(self.acc_id(csv_row), get_int(csv_row, self.vehicle_no_index))

    def id(self, csv_row):
        return common.get_usa_person_id(self.acc_id(csv_row), get_int(csv_row, self.vehicle_no_index),
                                        get_int(csv_row, self.person_no_index))

    def age(self, csv_row):
        age = get_int(csv_row, self.age_index)
        if self.year < 2009:
            if age == 99:
                age = -1
        else:
            if age > 997:
                age = -1
        return age

    def sex(self, csv_row):
        sex = get_int(csv_row, self.sex_index)
        if sex == 1:
            return 'MALE'
        elif sex == 2:
            return 'FEMALE'
        else:
            return 'UNKNOWN'

    def type(self, csv_row):
        type_int = get_int(csv_row, self.type_index)
        return fars_common.value_by_mapping(type_int, self.year, type_mapping())

    def injury_level(self, csv_row):
        injury_int = get_int(csv_row, self.injury_index)
        return fars_common.value_by_mapping(injury_int, self.year, injury_mapping())

    def seated_pos(self, csv_row):
        seated_pos_int = get_int(csv_row, self.seated_pos_index)
        return fars_common.value_by_mapping(seated_pos_int, self.year, seated_pos_mapping())

    def seatbelt(self, csv_row):
        seatbelt_int = get_int(csv_row, self.seatbelt_index)
        seatbelt_value = fars_common.value_by_mapping(seatbelt_int, self.year, seatbelt_mapping())
        if seatbelt_value == 'NOT_WORN_OR_NOT_APPLICABLE':
            if self.type(csv_row) == 'DRIVER' or self.type(csv_row) == 'PASSENGER':
                seatbelt_value = 'NOT_WORN'
            else:
                seatbelt_value = 'NOT_APPLICABLE'
        return seatbelt_value


# Helper functions
def get_int(list_row, index):
    if index < 0 or index > len(list_row) - 1:
        return -1
    else:
        return int(float(list_row[index]))


def get_float(list_row, index):
    if index < 0 or index > len(list_row) - 1:
        return -1.0
    else:
        return float(list_row[index])


def type_mapping():
    return {
        'default': 'UNKNOWN',
        1975: {
            1: 'DRIVER',
            2: 'PASSENGER',
            3: 'PEDESTRIAN'
        },
        1982: {
            1: 'DRIVER',
            2: 'PASSENGER',
            5: 'PEDESTRIAN'
        },
        1994: {
            1: 'DRIVER',
            2: 'PASSENGER',
            5: 'PEDESTRIAN'
        }
    }


def injury_mapping():
    return {
        'default': 'UNKNOWN',
        1975: {
            0: 'NONE',
            1: 'SLIGHT',
            2: 'SLIGHT',
            3: 'SERIOUS',
            4: 'FATAL',
            5: 'SLIGHT'
        }
    }


def seated_pos_mapping():
    return {
        'default': 'UNKNOWN',
        1975: {
            0: 'NONE',
            1: 'DRIVER',
            2: 'PASSENGER',
            3: 'PASSENGER',
            4: 'BACK',
            5: 'BACK',
            6: 'BACK',
            7: 'BACK',
            8: 'BACK',
            9: 'BACK',
            10: 'PASSENGER',
            11: 'BACK',
            12: 'BACK',
            13: 'BACK',
            14: 'BACK'
        },
        1982: {
            0: 'NONE',
            11: 'DRIVER',
            12: 'PASSENGER',
            13: 'PASSENGER',
            18: 'PASSENGER',
            19: 'PASSENGER',
            21: 'BACK',
            22: 'BACK',
            23: 'BACK',
            28: 'BACK',
            29: 'BACK',
            31: 'BACK',
            32: 'BACK',
            33: 'BACK',
            38: 'BACK',
            39: 'BACK',
            41: 'BACK',
            42: 'BACK',
            43: 'BACK',
            48: 'BACK',
            49: 'BACK',
            50: 'BACK',
            51: 'BACK',
            52: 'BACK',
            53: 'BACK',
            54: 'BACK',
        }
    }


def seatbelt_mapping():
    return {
        'default': 'UNKNOWN',
        1991: {
            0: 'NOT_WORN_OR_NOT_APPLICABLE',
            1: 'WORN_CONFIRMED',
            2: 'WORN_CONFIRMED',
            3: 'WORN_CONFIRMED'
        },
        1994: {
            0: 'NOT_WORN_OR_NOT_APPLICABLE',
            1: 'WORN_CONFIRMED',
            2: 'WORN_CONFIRMED',
            3: 'WORN_CONFIRMED',
            96: 'NOT_APPLICABLE'
        }
    }

