#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module handles mapping of rows from FARS data into common format.

Significant attributes:
ST_CASE - case ID
PERSONS
FATALS
VE_TOTAL - number of vehicles
YEAR
MONTH
DAY
DAY_WEEK
HOUR
MINUTE
LATITUDE
LONGITUD
"""
from parsing import fars_common
from parsing import common


class FARSAccidentMapper:
    def __init__(self, first_row):
        self.first_row = first_row
        # Check the indexes of significant fields
        self.st_case_index = self.index_of('ST_CASE')
        self.persons_index = self.index_of('PERSONS')
        self.fatalities_index = self.index_of('FATALS')
        self.vehicles_index = self.index_of('VE_TOTAL')
        self.year_index = self.index_of('YEAR')
        self.month_index = self.index_of('MONTH')
        self.day_index = self.index_of('DAY')
        self.day_of_week_index = self.index_of('DAY_WEEK')
        self.hour_index = self.index_of('HOUR')
        self.minute_index = self.index_of('MINUTE')
        self.latitude_index = self.index_of('LATITUDE')
        self.longitude_index = self.index_of('LONGITUD')
        self.speed_limit_index = self.index_of('SP_LIMIT')
        self.weather_index = self.index_of('WEATHER')
        self.weather1_index = self.index_of('WEATHER1')
        self.weather2_index = self.index_of('WEATHER2')

    def index_of(self, key):
        index = -1
        try:
            index = self.first_row.index(key)
        except ValueError:
            pass
        return index

    def valid(self, csv_row):
        return self.year(csv_row) > -1 and \
               self.month(csv_row) > -1 and \
               self.day(csv_row) > -1 and \
               self.hour(csv_row) > -1 and \
               self.minute(csv_row) > -1

    def id(self, csv_row):
        return common.get_usa_acc_id(self.year(csv_row), get_int(csv_row, self.st_case_index))

    def year(self, csv_row):
        year = get_int(csv_row, self.year_index)
        if year < 100:
            year += 1900
        return year

    def month(self, csv_row):
        month = get_int(csv_row, self.month_index)
        if month > 12:
            month = -1
        return month

    def day(self, csv_row):
        day = get_int(csv_row, self.day_index)
        if day > 31:
            day = -1
        return day

    def hour(self, csv_row):
        hour = get_int(csv_row, self.hour_index)
        if hour == 24:
            hour = 0
        if hour > 24:
            hour = -1
        return hour

    def minute(self, csv_row):
        minute = get_int(csv_row, self.minute_index)
        if minute > 59:
            minute = -1
        return minute

    def day_of_week(self, csv_row):
        day_of_week_int = get_int(csv_row, self.day_of_week_index)
        if day_of_week_int > 7:
            return -1
        else:
            return day_of_week_int

    def timestamp(self, csv_row):
        year = self.year(csv_row)
        month = self.month(csv_row)
        day = self.day(csv_row)
        hour = self.hour(csv_row)
        minute = self.minute(csv_row)
        return common.get_timestamp(year, month, day, hour, minute)

    def latitude(self, csv_row):
        return get_float(csv_row, self.latitude_index)

    def longitude(self, csv_row):
        return get_float(csv_row, self.longitude_index)

    def persons_count(self, csv_row):
        return get_int(csv_row, self.persons_index)

    def fatalities_count(self, csv_row):
        return get_int(csv_row, self.fatalities_index)

    def vehicles_count(self, csv_row):
        return get_int(csv_row, self.vehicles_index)

    def speed_limit(self, csv_row):
        return -1
        # TODO od 2009 te dane sa w VEHICLE, poza tym co robic z jednostka?
        # if self.year(csv_row) > 2009:
        # return -1
        # else:
        #     return get_int(csv_row, self.speed_limit)

    def snow(self, csv_row):
        return self.check_weather(csv_row, snow_mapping())

    def rain(self, csv_row):
        return self.check_weather(csv_row, rain_mapping())

    def wind(self, csv_row):
        return self.check_weather(csv_row, wind_mapping())

    def fog(self, csv_row):
        return self.check_weather(csv_row, fog_mapping())

    def relation_to_junction(self, csv_row):
        # TODO
        return 'UNKNOWN'

    def road_class(self, csv_row):
        # TODO
        return 'UNKNOWN'

    def surface_cond(self, csv_row):
        # TODO
        return 'UNKNOWN'

    def lighting(self, csv_row):
        # TODO
        return 'UNKNOWN'

    def traffic_control(self, csv_row):
        # TODO
        return 'UNKNOWN'

    def other_conditions(self, csv_row):
        # TODO
        return 'UNKNOWN'

    def check_weather(self, csv_row, weather_mapping):
        year = self.year(csv_row)
        weather_value_int = get_int(csv_row, self.weather_index)
        weather1_value_int = get_int(csv_row, self.weather1_index)
        weather2_value_int = get_int(csv_row, self.weather2_index)
        weather_value = fars_common.value_by_mapping(weather_value_int, year, weather_mapping)
        weather1_value = fars_common.value_by_mapping(weather1_value_int, year, weather_mapping)
        weather2_value = fars_common.value_by_mapping(weather2_value_int, year, weather_mapping)
        if weather_value == 'YES' or weather1_value == 'YES' or weather2_value == 'YES':
            return 'YES'
        elif weather_value == 'NO' or weather1_value == 'NO' or weather2_value == 'NO':
            return 'NO'
        else:
            return 'UNKNOWN'


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


def snow_mapping():
    return {
        'default': 'NO',
        1975: {
            3: 'YES',
            4: 'YES',
            9: 'UNKNOWN'
        },
        1980: {
            3: 'YES',
            4: 'YES',
            9: 'UNKNOWN'
        },
        1982: {
            3: 'YES',
            4: 'YES',
            9: 'UNKNOWN'
        },
        2007: {
            3: 'YES',
            4: 'YES',
            9: 'UNKNOWN'
        },
        2010: {
            3: 'YES',
            4: 'YES',
            11: 'YES',
            98: 'UNKNOWN',
            99: 'UNKNOWN'
        },
        2013: {
            3: 'YES',
            4: 'YES',
            11: 'YES',
            98: 'UNKNOWN',
            99: 'UNKNOWN'
        }
    }


def rain_mapping():
    return {
        'default': 'NO',
        1975: {
            2: 'YES',
            3: 'YES',
            9: 'UNKNOWN'
        },
        1980: {
            2: 'YES',
            3: 'YES',
            9: 'UNKNOWN'
        },
        1982: {
            2: 'YES',
            3: 'YES',
            6: 'YES',
            9: 'UNKNOWN'
        },
        2007: {
            2: 'YES',
            3: 'YES',
            9: 'UNKNOWN'
        },
        2010: {
            2: 'YES',
            3: 'YES',
            98: 'UNKNOWN',
            99: 'UNKNOWN'
        },
        2013: {
            2: 'YES',
            3: 'YES',
            12: 'YES',
            98: 'UNKNOWN',
            99: 'UNKNOWN'
        }
    }


def wind_mapping():
    return {
        'default': 'NO',
        1975: {
            9: 'UNKNOWN'
        },
        1980: {
            9: 'UNKNOWN'
        },
        1982: {
            9: 'UNKNOWN'
        },
        2007: {
            4: 'YES',
            6: 'YES',
            7: 'YES',
            9: 'UNKNOWN'
        },
        2010: {
            6: 'YES',
            7: 'YES',
            11: 'YES',
            98: 'UNKNOWN',
            99: 'UNKNOWN'
        },
        2013: {
            6: 'YES',
            7: 'YES',
            11: 'YES',
            98: 'UNKNOWN',
            99: 'UNKNOWN'
        }
    }


def fog_mapping():
    return {
        'default': 'NO',
        1975: {
            9: 'UNKNOWN'
        },
        1980: {
            5: 'YES',
            9: 'UNKNOWN'
        },
        1982: {
            5: 'YES',
            6: 'YES',
            7: 'YES',
            9: 'UNKNOWN'
        },
        2007: {
            5: 'YES',
            9: 'UNKNOWN'
        },
        2010: {
            5: 'YES',
            98: 'UNKNOWN',
            99: 'UNKNOWN'
        },
        2013: {
            5: 'YES',
            98: 'UNKNOWN',
            99: 'UNKNOWN'
        }
    }

