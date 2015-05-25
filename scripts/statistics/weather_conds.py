#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Time statistic for data.
"""

from scripts.db_api import accident


def query(country, snow, rain, wind, fog):
    country_clause = ''
    if country != '':
        country_clause = "country = '{0}' and".format(country)
    return '''
select count(*) from accident
    where {0}
    snow = '{1}' and
    rain = '{2}' and
    wind = '{3}' and
    fog = '{4}';
'''.format(country_clause, snow, rain, wind, fog)


if __name__ == '__main__':
    print('WTHR\tUSA\tGB\tUSA+GB')
    for snow in ['NO', 'YES']:
        for rain in ['NO', 'YES']:
            for wind in ['NO', 'YES']:
                for fog in ['NO', 'YES']:
                    conditions = ''
                    if snow == 'YES':
                        conditions += 'S'
                    if rain == 'YES':
                        conditions += 'R'
                    if wind == 'YES':
                        conditions += 'W'
                    if fog == 'YES':
                        conditions += 'F'
                    if conditions == '':
                        conditions = 'NONE'
                    usa_count = accident.execute_query(query('USA', snow, rain, wind, fog))[0][0]
                    gb_count = accident.execute_query(query('GB', snow, rain, wind, fog))[0][0]
                    both_count = accident.execute_query(query('', snow, rain, wind, fog))[0][0]
                    print('{0}\t{1}\t{2}\t{3}'.format(
                        conditions, usa_count, gb_count, both_count))
