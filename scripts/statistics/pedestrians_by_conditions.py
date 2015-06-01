#!/usr/bin/python
# -*- coding: utf-8 -*-

from scripts.db_api import accident


def general_query():
    return '''
SELECT count(*), (select count(*) from accident
    join person on(acc_id = accident.id)
    where country = 'USA'
    and person.type = 'PEDESTRIAN') as pedestrian
from accident
where country = 'USA';
'''

def rain_query():
    return '''
SELECT count(*), (select count(*) from accident
    join person on(acc_id = accident.id)
    where country = 'USA'
    and rain='YES'
    and person.type = 'PEDESTRIAN') as pedestrian
from accident
where country = 'USA'
and rain='YES';
'''

def snow_query():
    return '''
SELECT count(*), (select count(*) from accident
    join person on(acc_id = accident.id)
    where country = 'USA'
    and snow='YES'
    and person.type = 'PEDESTRIAN') as pedestrian
from accident
where country = 'USA'
and snow='YES';
'''

def fog_query():
    return '''
SELECT count(*), (select count(*) from accident
    join person on(acc_id = accident.id)
    where country = 'USA'
    and fog='YES'
    and person.type = 'PEDESTRIAN') as pedestrian
from accident
where country = 'USA'
and fog='YES';
'''

def dark_query():
    return '''
SELECT count(*), (select count(*) from accident
    join person on(acc_id = accident.id)
    where country = 'USA'
    and (lighting='DARK' or lighting='DARK_LIGHTED')
    and person.type = 'PEDESTRIAN') as pedestrian
from accident
where country = 'USA'
and (lighting='DARK' or lighting='DARK_LIGHTED');
'''


def get_value(age, dictionary):
    if age not in dictionary:
        return 0
    return dictionary[age]


if __name__ == '__main__':
    print('ALL\tPEDESTRIAN')
    usa_count = accident.execute_query(dark_query())
    print('{0}\t{1}\t'.format(usa_count[0][0], usa_count[0][1]))