#!/usr/bin/python
# -*- coding: utf-8 -*-

from scripts.db_api import accident


def general_query():
    return '''
SELECT count(*), (select count(*) from accident
    join vehicle on(acc_id = accident.id)
    where country = 'USA'
    and vehicle.speed > accident.speed_limit
    and vehicle.speed > -1
    and accident.speed_limit > 0) as exceeded
from accident
where country = 'USA';
'''

def rain_query():
    return '''
SELECT count(*), (select count(*) from accident
    join vehicle on(acc_id = accident.id)
    where country = 'USA'
    and vehicle.speed > accident.speed_limit
    and vehicle.speed > -1
    and accident.speed_limit > 0
    and rain='YES') as exceeded
from accident
where country = 'USA'
and rain='YES';
'''

def snow_query():
    return '''
SELECT count(*), (select count(*) from accident
    join vehicle on(acc_id = accident.id)
    where country = 'USA'
    and vehicle.speed > accident.speed_limit
    and vehicle.speed > -1
    and accident.speed_limit > 0
    and snow='YES') as exceeded
from accident
where country = 'USA'
and snow='YES';
'''

def fog_query():
    return '''
SELECT count(*), (select count(*) from accident
    join vehicle on(acc_id = accident.id)
    where country = 'USA'
    and vehicle.speed > accident.speed_limit
    and vehicle.speed > -1
    and accident.speed_limit > 0
    and fog='YES') as exceeded
from accident
where country = 'USA'
and fog='YES';
'''

def dark_query():
    return '''
SELECT count(*), (select count(*) from accident
    join vehicle on(acc_id = accident.id)
    where country = 'USA'
    and vehicle.speed > accident.speed_limit
    and vehicle.speed > -1
    and accident.speed_limit > 0
    and (lighting='DARK' or lighting='DARK_LIGHTED')) as exceeded
from accident
where country = 'USA'
and (lighting='DARK' or lighting='DARK_LIGHTED');
'''


def get_value(age, dictionary):
    if age not in dictionary:
        return 0
    return dictionary[age]


if __name__ == '__main__':
    print('ALL\texceeded')
    usa_count = accident.execute_query(general_query())
    print('{0}\t{1}\t'.format(usa_count[0][0], usa_count[0][1]))
    usa_count = accident.execute_query(rain_query())
    print('{0}\t{1}\t'.format(usa_count[0][0], usa_count[0][1]))
    usa_count = accident.execute_query(snow_query())
    print('{0}\t{1}\t'.format(usa_count[0][0], usa_count[0][1]))
    usa_count = accident.execute_query(fog_query())
    print('{0}\t{1}\t'.format(usa_count[0][0], usa_count[0][1]))
    usa_count = accident.execute_query(dark_query())
    print('{0}\t{1}\t'.format(usa_count[0][0], usa_count[0][1]))