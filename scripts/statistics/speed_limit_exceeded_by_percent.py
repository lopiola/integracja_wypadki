#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import defaultdict

from scripts.db_api import accident


def usa_query():
    return '''
select vehicle.speed, accident.speed_limit from accident
    join vehicle on(acc_id = accident.id)
    where country = 'USA'
    and vehicle.speed > -1
    and accident.speed_limit > 0
'''


def get_value(age, dictionary):
    if age not in dictionary:
        return 0
    return dictionary[age]

def get_bounds(percentage):
    if percentage <= 0:
        return '<=0%'
    return '{0}-{1}%'.format((percentage / 10) * 10, (percentage / 10 + 1) * 10)

if __name__ == '__main__':
    print('DAY\tALL\tEXCEEDED')
    usa_count = accident.execute_query(usa_query())
    # print('{0}\t{1}'.format(usa_count[0][0], usa_count[0][1]))
    percentage_dict = defaultdict(int)
    for speed, limit in usa_count:
        percentage = (speed * 100 / limit) - 100
        if percentage <= 600:
            percentage_dict[get_bounds(percentage)] += 1

    for key, value in percentage_dict.iteritems():
        print key, value

    for i in xrange(0, 600, 10):
        print get_bounds(i), percentage_dict[get_bounds(i)]