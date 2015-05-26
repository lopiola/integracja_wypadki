#!/usr/bin/python
# -*- coding: utf-8 -*-

from scripts.db_api import accident


def usa_query(day_of_week):
    return '''
SELECT count(*), (select count(*) from accident
    join vehicle on(acc_id = accident.id)
    where country = 'USA'
    and vehicle.speed > accident.speed_limit
    and vehicle.speed > -1
    and accident.speed_limit > 0
    and day_of_week = {0}) as exceeded
from accident
where country = 'USA' and day_of_week = {0};
'''.format(day_of_week)


def get_value(age, dictionary):
    if age not in dictionary:
        return 0
    return dictionary[age]


if __name__ == '__main__':
    print('DAY\tALL\tEXCEEDED')
    for i in xrange(1, 8):
        usa_count = accident.execute_query(usa_query(i))
        print('{0}\t{1}\t{2}'.format(i, usa_count[0][0], usa_count[0][1]))
