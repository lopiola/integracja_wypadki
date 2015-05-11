#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module handles mapping of rows from FARS data into common format.

Significant attributes:
ST_CASE - case ID
VEH_NO - vehicle
NUMOCCS - number of occupants
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

    def valid(self, csv_row):
        return True

    def index_of(self, key):
        index = -1
        try:
            index = self.first_row.index(key)
        except ValueError:
            pass
        return index

    def acc_id(self, csv_row):
        return common.get_usa_acc_id(self.year, get_int(csv_row, self.st_case_index))

    def id(self, csv_row):
        return common.get_usa_veh_id(self.acc_id(csv_row), get_int(csv_row, self.vehicle_no_index))

    def driver_sex(self, csv_row, driver_per_veh):
        veh_id = self.id(csv_row)
        if veh_id not in driver_per_veh:
            return 'UNKNOWN'
        else:
            driver = driver_per_veh[veh_id]
            if driver is None:
                return 'UNKNOWN'
            else:
                return driver['sex']

    def driver_age(self, csv_row, driver_per_veh):
        veh_id = self.id(csv_row)
        if veh_id not in driver_per_veh:
            return -1
        else:
            driver = driver_per_veh[veh_id]
            if driver is None:
                return -1
            else:
                return driver['age']

    def passenger_count(self, csv_row):
        return get_int(csv_row, self.occupants_index)


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

