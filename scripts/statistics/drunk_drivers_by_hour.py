#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Time statistic for data.
"""

from scripts.db_api import accident


def usa_query(hour):
    return '''
SELECT
    count(*),
    (SELECT count(*) from
        (SELECT count(*) from accident join vehicle on(acc_id = accident.id)
            where country = 'USA' and date_part('hour', timestamp) = {0} and driver_drinking = 'YES'
            group by accident.id) as sq) as drunk
from accident
where country = 'USA' and date_part('hour', timestamp) = {0};
'''.format(hour)


def get_value(age, dictionary):
    if age not in dictionary:
        return 0
    return dictionary[age]


if __name__ == '__main__':
    print('HOUR\tALL\tDRUNK')
    for i in xrange(0, 24):
        usa_count = accident.execute_query(usa_query(i))
        print('{0}\t{1}\t{2}'.format(i, usa_count[0][0], usa_count[0][1]))
