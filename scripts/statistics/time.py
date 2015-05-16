#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Time statistic for data.
"""

from scripts.db_api import accident

def yearly_statistics():
    return time_statistics('year')

def monthly_statistics():
    return time_statistics('month')

def time_statistics(time_period='year'):
    return accident.execute_query(time_statistics_query().format(time_period=time_period))


def time_statistics_query():
    return '''
select date_part('{time_period}', timestamp), count(*) from accident
group by date_part('{time_period}', timestamp)
order by date_part('{time_period}', timestamp);
'''


if __name__ == '__main__':
    for (year, count) in yearly_statistics():
        print int(year), count

    # for (month, count) in monthly_statistics():
    #     print int(month), count