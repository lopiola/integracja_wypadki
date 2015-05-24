#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Time statistic for data.
"""

from scripts.db_api import accident


def gb_query():
    return '''
select age, count(age) from person join accident on (acc_id = accident.id)
where country = 'GB'
group by age
order by age;
'''


def usa_query():
    return '''
select age, count(age) from person join accident on (acc_id = accident.id)
where country = 'USA'
group by age
order by age;
'''


def all_query():
    return '''
select age, count(age) from person
group by age
order by age;
'''


def get_value(age, dictionary):
    if age not in dictionary:
        return 0
    return dictionary[age]


if __name__ == '__main__':
    print('AGE\tUSA\tGB\tUSA+GB')
    usa_count = dict(accident.execute_query(usa_query()))
    gb_count = dict(accident.execute_query(gb_query()))
    all_count = dict(accident.execute_query(all_query()))
    for i in xrange(-1, 200):
        if i not in usa_count and i not in gb_count and i not in all_count:
            continue
        print('{0}\t{1}\t{2}\t{3}'.format(i, get_value(i, usa_count), get_value(i, gb_count), get_value(i, all_count)))