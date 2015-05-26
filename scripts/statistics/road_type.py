#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Road type statistics.
"""

from scripts.db_api import accident


def gb_query():
    return '''
select road_class, count(id) from accident
where country = 'GB'
group by road_class;
'''


def usa_query():
    return '''
select road_class, count(id) from accident
where country = 'USA'
group by road_class;
'''


def all_query():
    return '''
select road_class, count(id) from accident
group by road_class;
'''


def get_value(age, dictionary):
    if age not in dictionary:
        return 0
    return dictionary[age]


if __name__ == '__main__':
    print('ROAD_TYPE\tUSA\tGB\tUSA+GB')
    usa_count = dict(accident.execute_query(usa_query()))
    gb_count = dict(accident.execute_query(gb_query()))
    all_count = dict(accident.execute_query(all_query()))
    for road_class in ['MOTORWAY', 'PRINCIPAL', 'MAJOR', 'MINOR', 'UNCLASSIFIED', 'UNKNOWN']:
        if road_class in ['MOTORWAY', 'PRINCIPAL', 'UNCLASSIFIED']:
            print('{0}\t{1}\t{2}\t{3}'.format(road_class, get_value(road_class, usa_count), get_value(road_class, gb_count), get_value(road_class, all_count)))
        else:
            print('{0}\t\t{1}\t{2}\t{3}'.format(road_class, get_value(road_class, usa_count), get_value(road_class, gb_count), get_value(road_class, all_count)))