#!/usr/bin/python
# -*- coding: utf-8 -*-

from scripts.db_api import accident


def usa_query(day, month):
    return '''
SELECT count(*), (select count(*) from accident
    join vehicle on(acc_id = accident.id)
    where country = 'USA' and date_part('day', timestamp) = {0}
        and date_part('month', timestamp) = {1}
        and vehicle.speed > accident.speed_limit
        and vehicle.speed > -1
        and accident.speed_limit > 0) as exceeded
from accident
where country = 'USA' and date_part('day', timestamp) = {0}
        and date_part('month', timestamp) = {1};
'''.format(day, month)


def get_value(age, dictionary):
    if age not in dictionary:
        return 0
    return dictionary[age]


if __name__ == '__main__':
    print('DAY\tALL\tEXCEEDED')
    month_lengths = {
        1: 31,
        2: 29,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31
    }
    for month in xrange(1, 13):
        for day in xrange(1, month_lengths[month] + 1):
            usa_count = accident.execute_query(usa_query(day, month))
            print('{0}.{1}\t{2}\t{3}'.format(int(day), int(month), usa_count[0][0], usa_count[0][1]))
