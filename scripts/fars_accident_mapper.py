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
ROAD_FCN
"""
from parsing import fars_common
from parsing import common


class FARSAccidentMapper:
    def __init__(self, first_row, year):
        self.year = year
        self.first_row = first_row
        # Check the indexes of significant fields
        self.st_case_index = self.index_of('ST_CASE')
        self.persons_index = self.index_of('PERSONS')
        self.fatalities_index = self.index_of('FATALS')
        self.year_index = self.index_of('YEAR')
        self.month_index = self.index_of('MONTH')
        self.day_index = self.index_of('DAY')
        self.day_of_week_index = self.index_of('DAY_WEEK')
        self.hour_index = self.index_of('HOUR')
        self.minute_index = self.index_of('MINUTE')
        self.speed_limit_index = self.index_of('SP_LIMIT')
        self.road_class_index = self.index_of('ROAD_FNC')
        self.surface_cond_index = self.index_of('SUR_COND')
        self.lighting_index = self.index_of('LGT_COND')
        self.weather_index = self.index_of('WEATHER')

        self.weather1_index = -1
        self.weather2_index = -1
        if year > 2006:
            self.weather1_index = self.index_of('WEATHER1')
            self.weather2_index = self.index_of('WEATHER2')

        self.latitude_index = -1
        if year > 1998:
            self.latitude_index = self.index_of('LATITUDE')

        self.longitude_index = -1
        if year > 1998:
            self.longitude_index = self.index_of('LONGITUD')

        self.rel_to_junction_index = -1
        if year < 2010:
            self.rel_to_junction_index = self.index_of('REL_JUNC')
        else:
            self.rel_to_junction_index = self.index_of('RELJCT2')

        self.traffic_control_index = -1
        if year < 2010:
            self.traffic_control_index = self.index_of('TRA_CONT')

        self.signal_malf_index = -1
        if 1981 < year < 2010:
            self.signal_malf_index = self.index_of('T_CONT_F')

    def index_of(self, key):
        index = -1
        try:
            index = self.first_row.index(key)
        except ValueError:
            print('WARNING [ACC {0}]: Cannot find index of {1}'
                  .format(self.year, key))
            pass
        return index

    def valid(self, csv_row, vehicles_by_acc):
        date_valid = self.year > -1 and \
            self.month(csv_row) > -1 and \
            self.day(csv_row) > -1 and \
            self.hour(csv_row) > -1 and \
            self.minute(csv_row) > -1
        are_there_vehicles = self.id(csv_row) in vehicles_by_acc
        return date_valid and are_there_vehicles

    def id(self, csv_row):
        return common.get_usa_acc_id(self.year, fars_common.get_int(csv_row, self.st_case_index))

    def month(self, csv_row):
        month = fars_common.get_int(csv_row, self.month_index)
        if month > 12:
            month = -1
        return month

    def day(self, csv_row):
        day = fars_common.get_int(csv_row, self.day_index)
        if day > 31:
            day = -1
        return day

    def hour(self, csv_row):
        hour = fars_common.get_int(csv_row, self.hour_index)
        if hour == 24:
            hour = 0
        if hour > 24:
            hour = -1
        return hour

    def minute(self, csv_row):
        minute = fars_common.get_int(csv_row, self.minute_index)
        if minute > 59:
            minute = -1
        return minute

    def day_of_week(self, csv_row):
        day_of_week_int = fars_common.get_int(csv_row, self.day_of_week_index)
        if day_of_week_int > 7:
            return -1
        else:
            return day_of_week_int

    def timestamp(self, csv_row):
        year = self.year
        month = self.month(csv_row)
        day = self.day(csv_row)
        hour = self.hour(csv_row)
        minute = self.minute(csv_row)
        return common.get_timestamp(year, month, day, hour, minute)

    def latitude(self, csv_row):
        if self.latitude_index == -1:
            return 200.0
        value = fars_common.get_float(csv_row, self.latitude_index)
        if value == -1.0 or value == 0.0:
            return 200.0
        initial_value = value
        if self.year < 2001:
            if value >= 88888888:
                return 200.0
            degrees = value // 1000000
            minutes = (value % 1000000) / 10000
            seconds = (value % 10000) / 100
            value = degrees + minutes / 60 + seconds / 3600

        if not 15 < value < 75:
            print('WARNING [{0}]: latitude parsing gave {1} -> {2}'
                  .format(self.year, initial_value, value))
        return value

    def longitude(self, csv_row):
        if self.longitude_index == -1:
            return 200.0
        value = fars_common.get_float(csv_row, self.longitude)
        if value == -1.0 or value == 0.0:
            return 200.0
        initial_value = value
        if self.year < 2001:
            if value >= 888888888:
                return 200.0
            degrees = value // 1000000
            minutes = (value % 1000000) / 10000
            seconds = (value % 10000) / 100
            value = degrees + minutes / 60 + seconds / 3600

        if not 60 < value < 180.0:
            print('WARNING [{0}]: longitude parsing gave {1} -> {2}'
                  .format(self.year, initial_value, value))
        return value

    def persons_count(self, csv_row):
        return fars_common.get_int(csv_row, self.persons_index)

    def fatalities_count(self, csv_row):
        return fars_common.get_int(csv_row, self.fatalities_index)

    def vehicles_count(self, csv_row, vehicles_by_acc):
        return len(vehicles_by_acc[self.id(csv_row)])

    def speed_limit(self, csv_row, speed_limits_by_acc):
        value = fars_common.get_int(csv_row, self.speed_limit_index)
        if self.year > 2009:
            vehicles = speed_limits_by_acc[self.id(csv_row)]
            speed_limit = 100
            for curr_speed_limit in vehicles:
                if 0 < curr_speed_limit < speed_limit:
                    speed_limit = curr_speed_limit
            if speed_limit == 100:
                speed_limit = -1
            value = speed_limit
        mph_value = value
        if value == 99:
            mph_value = -1
        if self.year < 1979:
            if value == 96:
                mph_value = -1
            if value == 98:
                mph_value = -1
        if mph_value == -1:
            return -1
        return common.mph_to_kmph(mph_value)

    def snow(self, csv_row):
        return self.check_weather(csv_row, snow_mapping())

    def rain(self, csv_row):
        return self.check_weather(csv_row, rain_mapping())

    def wind(self, csv_row):
        return self.check_weather(csv_row, wind_mapping())

    def fog(self, csv_row):
        return self.check_weather(csv_row, fog_mapping())

    def relation_to_junction(self, csv_row):
        value = fars_common.get_int(csv_row, self.rel_to_junction_index)
        return fars_common.value_by_mapping(value, self.year, rel_to_junction_mapping())

    def road_class(self, csv_row):
        value = fars_common.get_int(csv_row, self.road_class_index)
        return fars_common.value_by_mapping(value, self.year, road_class_mapping())

    def surface_cond(self, csv_row, surface_conds_by_acc):
        value = fars_common.get_int(csv_row, self.surface_cond_index)
        value_str = fars_common.value_by_mapping(value, self.year, surface_cond_mapping())
        if self.year > 2009:
            hierarchy = {
                'UNKNOWN': 0,
                'DRY': 1,
                'WET': 2,
                'OTHER': 3,
                'FLOOD': 4,
                'SNOW': 5,
                'ICE': 6
            }
            value_str = 'UNKNOWN'
            for current_value in surface_conds_by_acc[self.id(csv_row)]:
                if hierarchy[current_value] > hierarchy[value_str]:
                    value_str = current_value
        return value_str

    def lighting(self, csv_row):
        value = fars_common.get_int(csv_row, self.lighting_index)
        return fars_common.value_by_mapping(value, self.year, lighting_mapping())

    def traffic_control(self, csv_row, traffic_controls_by_acc):
        value_str = 'UNKNOWN'
        if self.year < 2010:
            value = fars_common.get_int(csv_row, self.traffic_control_index)
            value_str = fars_common.value_by_mapping(value, self.year, traffic_control_mapping())
            signal_malf_value = fars_common.get_int(csv_row, self.signal_malf_index)
            if signal_malf_value == 1 or signal_malf_value == 2:
                value_str = 'SIGNAL_MALF'
        else:
            hierarchy = {
                'UNKNOWN': 0,
                'YIELD_OR_NONE': 1,
                'TRAFFIC_SIGNAL': 2,
                'STOP_SIGN': 3,
                'SIGNAL_MALF': 4,
                'AUTH_PERSON': 5
            }
            for current_value in traffic_controls_by_acc[self.id(csv_row)]:
                if hierarchy[current_value] > hierarchy[value_str]:
                    value_str = current_value
        return value_str

    def other_conditions(self, csv_row):
        return 'UNKNOWN'

    def check_weather(self, csv_row, weather_mapping):
        year = self.year
        weather_value_int = fars_common.get_int(csv_row, self.weather_index)
        weather1_value_int = fars_common.get_int(csv_row, self.weather1_index)
        weather2_value_int = fars_common.get_int(csv_row, self.weather2_index)
        weather_value = fars_common.value_by_mapping(weather_value_int, year, weather_mapping)
        weather1_value = fars_common.value_by_mapping(weather1_value_int, year, weather_mapping)
        weather2_value = fars_common.value_by_mapping(weather2_value_int, year, weather_mapping)
        if weather_value == 'YES' or weather1_value == 'YES' or weather2_value == 'YES':
            return 'YES'
        elif weather_value == 'NO' or weather1_value == 'NO' or weather2_value == 'NO':
            return 'NO'
        else:
            return 'UNKNOWN'


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


def rel_to_junction_mapping():
    return {
        'default': 'UNKNOWN',
        1975: {
            1: 'NON_JUNCTION',
            2: 'INTERSECTION',
            3: 'INTERSECTION',
            4: 'INTERSECTION',
            5: 'DRIVEWAY',
            6: 'RAMP',
            7: 'NON_JUNCTION',
            8: 'INTERSECTION'
        },
        1991: {
            0: 'NON_JUNCTION',
            1: 'NON_JUNCTION',
            2: 'INTERSECTION',
            3: 'INTERSECTION',
            4: 'DRIVEWAY',
            5: 'RAMP',
            6: 'NON_JUNCTION',
            7: 'INTERSECTION',
            8: 'DRIVEWAY',
            10: 'INTERSECTION',
            11: 'INTERSECTION',
            12: 'DRIVEWAY',
            13: 'RAMP',
            14: 'INTERSECTION',
            15: 'INTERSECTION',
            19: 'INTERSECTION'
        }
    }


def road_class_mapping():
    return {
        'default': 'UNKNOWN',
        1981: {
            1: 'PRINCIPAL',
            2: 'MOTORWAY',
            3: 'PRINCIPAL',
            4: 'MINOR',
            5: 'MINOR',
            6: 'MAJOR',
            7: 'MINOR',
            8: 'MINOR'
        },
        1987: {
            1: 'PRINCIPAL',
            2: 'PRINCIPAL',
            3: 'MINOR',
            4: 'MAJOR',
            5: 'MINOR',
            6: 'MINOR',
            11: 'PRINCIPAL',
            12: 'MOTORWAY',
            13: 'PRINCIPAL',
            14: 'MINOR',
            15: 'MAJOR',
            16: 'MINOR'
        }
    }


def surface_cond_mapping():
    return {
        'default': 'UNKNOWN',
        2010: {
            1: 'DRY',
            2: 'WET',
            3: 'SNOW',
            4: 'ICE',
            5: 'OTHER',
            6: 'FLOOD',
            7: 'OTHER',
            8: 'OTHER'
        }
    }


def lighting_mapping():
    return {
        'default': 'UNKNOWN',
        1975: {
            1: 'DAYLIGHT',
            2: 'DARK',
            3: 'DARK_LIGHTED',
            4: 'DAYLIGHT',
            5: 'DAYLIGHT',
            6: 'DAYLIGHT'
        },
        1980: {
            1: 'DAYLIGHT',
            2: 'DARK',
            3: 'DARK_LIGHTED',
            4: 'DAYLIGHT',
            5: 'DAYLIGHT',
            6: 'DARK'
        }
    }


def traffic_control_mapping():
    return {
        'default': 'UNKNOWN',
        1975: {
            0: 'YIELD_OR_NONE',
            1: 'TRAFFIC_SIGNAL',
            2: 'TRAFFIC_SIGNAL',
            3: 'STOP_SIGN',
            4: 'YIELD_OR_NONE',
            9: 'SIGNAL_MALF'
        },
        1982: {
            0: 'YIELD_OR_NONE',
            1: 'TRAFFIC_SIGNAL',
            2: 'TRAFFIC_SIGNAL',
            3: 'TRAFFIC_SIGNAL',
            4: 'TRAFFIC_SIGNAL',
            5: 'TRAFFIC_SIGNAL',
            6: 'TRAFFIC_SIGNAL',
            7: 'TRAFFIC_SIGNAL',
            8: 'TRAFFIC_SIGNAL',
            9: 'TRAFFIC_SIGNAL',
            20: 'STOP_SIGN',
            21: 'YIELD_OR_NONE',
            50: 'AUTH_PERSON',
        }
    }


