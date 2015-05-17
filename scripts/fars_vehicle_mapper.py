#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module handles mapping of rows from FARS data into common format.

Significant attributes:
ST_CASE - case ID
VEH_NO - vehicle
NUMOCCS - number of occupants
BODY_TYP
"""

from parsing import fars_common
from parsing import common


class FARSVehicleMapper:
    def __init__(self, first_row, year):
        self.first_row = first_row
        self.year = year
        # Check the indexes of significant fields
        self.st_case_index = self.index_of('ST_CASE')
        self.vehicle_no_index = self.index_of('VEH_NO')
        self.occupants_index = self.index_of('NUMOCCS')
        self.type_index = self.index_of('BODY_TYP')
        self.fuel_index = self.index_of('FLDCD_TR')
        if year > 2009:
            self.fuel_index = self.index_of('FUELCODE')
        self.hit_n_run_index = self.index_of('HIT_RUN')
        self.skidded_index = self.index_of('PCRASH4')
        self.rollover_index = self.index_of('ROLLOVER')
        self.jackknifing_index = self.index_of('J_KNIFE')
        self.impact_area = self.index_of('IMPACT1')
        self.maneuver_index = self.index_of('J_KNIFE')


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

    def id(self, csv_row):
        return common.get_usa_veh_id(self.acc_id(csv_row), get_int(csv_row, self.vehicle_no_index))

    def driver_sex(self, csv_row, driver_by_veh):
        veh_id = self.id(csv_row)
        if veh_id not in driver_by_veh:
            return 'UNKNOWN'
        else:
            driver = driver_by_veh[veh_id]
            if driver is None:
                return 'UNKNOWN'
            else:
                return driver['sex']

    def driver_age(self, csv_row, driver_by_veh):
        veh_id = self.id(csv_row)
        if veh_id not in driver_by_veh:
            return -1
        else:
            driver = driver_by_veh[veh_id]
            if driver is None:
                return -1
            else:
                return driver['age']

    def passenger_count(self, csv_row):
        return get_int(csv_row, self.occupants_index)

    def type(self, csv_row):
        type_int = get_int(csv_row, self.type_index)
        return fars_common.value_by_mapping(type_int, self.year, type_mapping())

    def fuel_type(self, csv_row):
        fuel_code = get_str(csv_row, self.fuel_index)
        return fars_common.value_by_mapping(fuel_code, self.year, fuel_mapping())

    def hit_and_run(self, csv_row):
        value = get_int(csv_row, self.hit_n_run_index)
        return fars_common.value_by_mapping(value, self.year, hit_n_run_mapping())

    def skidded(self, csv_row):
        value = get_int(csv_row, self.skidded_index)
        return fars_common.value_by_mapping(value, self.year, skidded_mapping())

    def rollover(self, csv_row):
        value = get_int(csv_row, self.rollover_index)
        return fars_common.value_by_mapping(value, self.year, rollover_mapping())

    def jackknifing(self, csv_row):
        value = get_int(csv_row, self.jackknifing_index)
        return fars_common.value_by_mapping(value, self.year, jack_knifing_mapping())

    def first_impact_area(self, csv_row):
        value = get_int(csv_row, self.impact_area)
        return fars_common.value_by_mapping(value, self.year, impact_mapping())

    def maneuver(self, csv_row):
        value = get_int(csv_row, self.maneuver_index)
        return fars_common.value_by_mapping(value, self.year, impact_mapping())


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


def get_str(list_row, index):
    if index < 0 or index > len(list_row) - 1:
        return 'UNKNOWN'
    else:
        return list_row[index]


def type_mapping():
    return {
        'default': 'OTHER',
        1975: {
            1: 'CAR',
            2: 'CAR',
            3: 'CAR',
            4: 'CAR',
            5: 'CAR',
            6: 'CAR',
            7: 'CAR',
            8: 'CAR',
            9: 'CAR',
            15: 'MOTORCYCLE',
            16: 'MOTORCYCLE',
            17: 'MOTORCYCLE',
            18: 'MOTORCYCLE',
            25: 'BUS',
            26: 'BUS',
            27: 'BUS',
            28: 'BUS',
            29: 'BUS',
            36: 'AGRICULTURAL',
            37: 'AGRICULTURAL',
            43: 'CAR',
            51: 'CARGO',
            52: 'CARGO',
            53: 'CARGO',
            54: 'CARGO',
            55: 'CARGO',
            56: 'CARGO',
            57: 'CARGO',
            58: 'CARGO',
            59: 'CARGO',
            60: 'CARGO',
            99: 'UNKNOWN'
        },
        1982: {
            1: 'CAR',
            2: 'CAR',
            3: 'CAR',
            4: 'CAR',
            5: 'CAR',
            6: 'CAR',
            7: 'CAR',
            8: 'CAR',
            9: 'CAR',
            10: 'CARGO',
            20: 'MOTORCYCLE',
            21: 'MOTORCYCLE',
            27: 'MOTORCYCLE',
            28: 'MOTORCYCLE',
            29: 'MOTORCYCLE',
            30: 'BUS',
            31: 'BUS',
            32: 'BUS',
            38: 'BUS',
            39: 'BUS',
            40: 'CARGO',
            41: 'CARGO',
            42: 'CARGO',
            48: 'CARGO',
            49: 'CARGO',
            50: 'CARGO',
            51: 'CARGO',
            52: 'CARGO',
            53: 'CARGO',
            54: 'CARGO',
            55: 'CARGO',
            56: 'CARGO',
            58: 'CARGO',
            59: 'CARGO',
            67: 'CARGO',
            69: 'CARGO',
            70: 'CARGO',
            71: 'CARGO',
            72: 'CARGO',
            73: 'CARGO',
            74: 'CARGO',
            75: 'CARGO',
            76: 'CARGO',
            77: 'CARGO',
            78: 'CARGO',
            79: 'CARGO',
            81: 'AGRICULTURAL',
            82: 'AGRICULTURAL',
            99: 'UNKNOWN'
        },
        1991: {
            1: 'CAR',
            2: 'CAR',
            3: 'CAR',
            4: 'CAR',
            5: 'CAR',
            6: 'CAR',
            7: 'CAR',
            8: 'CAR',
            9: 'CAR',
            10: 'CARGO',
            13: 'CAR',
            17: 'CAR',
            20: 'CARGO',
            21: 'CARGO',
            22: 'CARGO',
            24: 'BUS',
            25: 'BUS',
            28: 'CARGO',
            29: 'CARGO',
            30: 'CARGO',
            31: 'CARGO',
            32: 'CARGO',
            33: 'CARGO',
            39: 'CARGO',
            41: 'CARGO',
            42: 'CARGO',
            45: 'CARGO',
            48: 'CARGO',
            49: 'CARGO',
            50: 'BUS',
            51: 'BUS',
            52: 'BUS',
            55: 'BUS',
            58: 'BUS',
            59: 'BUS',
            60: 'CARGO',
            61: 'CARGO',
            62: 'CARGO',
            63: 'CARGO',
            64: 'CARGO',
            65: 'CARGO',
            66: 'CARGO',
            67: 'CARGO',
            68: 'CARGO',
            71: 'CARGO',
            72: 'CARGO',
            73: 'CARGO',
            78: 'CARGO',
            79: 'CARGO',
            80: 'MOTORCYCLE',
            81: 'MOTORCYCLE',
            82: 'MOTORCYCLE',
            83: 'MOTORCYCLE',
            88: 'MOTORCYCLE',
            89: 'MOTORCYCLE',
            92: 'AGRICULTURAL',
            98: 'UNKNOWN',
            99: 'UNKNOWN'
        }
    }


def fuel_mapping():
    return {
        'default': 'UNKNOWN',
        1975: {
            'B': 'HYBRID',
            'C': 'PETROL',
            'D': 'DIESEL',
            'E': 'OTHER',
            'G': 'GAS',
            'H': 'OTHER',
            'M': 'OTHER',
            'N': 'GAS',
            'P': 'GAS',
        }
    }


def hit_n_run_mapping():
    return {
        'default': 'NO',
        1975: {
            1: 'YES',
            2: 'YES',
            3: 'YES',
            4: 'YES',
            5: 'YES'
        },
        2009: {
            1: 'YES',
            8: 'UNKNOWN',
            9: 'UNKNOWN',
        }
    }


def jack_knifing_mapping():
    return {
        'default': 'UNKNOWN',
        1975: {
            0: 'NO',
            1: 'NO',
            2: 'YES',
            3: 'YES'
        }
    }


def skidded_mapping():
    return {
        'default': 'UNKNOWN',
        2010: {
            1: 'NO',
            2: 'YES',
            3: 'YES',
            4: 'YES',
            5: 'YES',
            7: 'NO'
        }
    }


def rollover_mapping():
    return {
        'default': 'UNKNOWN',
        1979: {
            0: 'NO',
            1: 'YES',
            2: 'YES',
            9: 'YES'
        }
    }


def impact_mapping():
    return {
        'default': 'UNKNOWN',
        1979: {
            0: 'NON_COLLISION',
            11: 'FRONT',
            12: 'FRONT',
            1: 'FRONT',
            5: 'BACK',
            6: 'BACK',
            7: 'BACK',
            2: 'RIGHT_SIDE',
            3: 'RIGHT_SIDE',
            4: 'RIGHT_SIDE',
            8: 'LEFT_SIDE',
            9: 'LEFT_SIDE',
            10: 'LEFT_SIDE',
            61: 'LEFT_SIDE',
            62: 'LEFT_SIDE',
            63: 'LEFT_SIDE',
            81: 'RIGHT_SIDE',
            82: 'RIGHT_SIDE',
            83: 'RIGHT_SIDE'
        }
    }