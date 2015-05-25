#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Time statistic for data.
"""

from scripts.db_api import accident


def gb_query():
    return '''
select date_part('day', timestamp) as day, date_part('month', timestamp) as month, count(*) as count from accident
where country = 'GB'
group by month, day
order by month, day
'''


def usa_query():
    return '''
select date_part('day', timestamp) as day, date_part('month', timestamp) as month, count(*) as count from accident
where country = 'USA'
group by month, day
order by month, day
'''


def all_query():
    return '''
select date_part('day', timestamp) as day, date_part('month', timestamp) as month, count(*) as count from accident
group by month, day
order by month, day
'''


def get_value(age, dictionary):
    if age not in dictionary:
        return 0
    return dictionary[age]


if __name__ == '__main__':
    print('DAY\tUSA\tGB\tUSA+GB')
    usa_count = accident.execute_query(usa_query())
    gb_count = accident.execute_query(gb_query())
    all_count = accident.execute_query(all_query())
    for i in xrange(0, len(usa_count)):
        print('{0}.{1}\t{2}\t{3}\t{4}'.format(
            int(usa_count[i][0]), int(usa_count[i][1]), usa_count[i][2], gb_count[i][2], all_count[i][2]))