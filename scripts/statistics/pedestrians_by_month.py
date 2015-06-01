#!/usr/bin/python
# -*- coding: utf-8 -*-

from scripts.db_api import accident


def usa_query(month):
    return '''
SELECT count(*), (select count(*) from accident
    join person on(acc_id = accident.id)
    where country = 'USA'
    and person.type = 'PEDESTRIAN'
    and date_part('month', timestamp) = {0}) as pedestrian
from accident
where country = 'USA' and date_part('month', timestamp) = {0};
'''.format(month)


def get_value(age, dictionary):
    if age not in dictionary:
        return 0
    return dictionary[age]


if __name__ == '__main__':
    print('MONTH\tALL\tPEDESTRIAN')
    for i in xrange(1, 13):
        usa_count = accident.execute_query(usa_query(i))
        print('{0}\t{1}\t{2}'.format(i, usa_count[0][0], usa_count[0][1]))