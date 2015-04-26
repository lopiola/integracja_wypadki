#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Manipulates the accident table
"""

from psycopg2 import connect

import common


def add(accident_list):
    user = common.get_user()
    database = common.get_db_name()
    con = connect(user=user, database=database)
    cur = con.cursor()

    for accident in accident_list:
        command = '''
INSERT INTO accident VALUES (
{id},
{timestamp},
{day_of_week},
{latitude},
{longtitude},
{persons_count},
{fatalities_count},
{vehicles_count},
{speed_limit}
);
'''
        command = command.format(
            id=accident['id'],
            timestamp=accident['timestamp'],
            day_of_week=accident['day_of_week'],
            latitude=accident['latitude'],
            longtitude=accident['longtitude'],
            persons_count=accident['persons_count'],
            fatalities_count=accident['fatalities_count'],
            vehicles_count=accident['vehicles_count'],
            speed_limit=accident['speed_limit']
        )
        cur.execute(command)

    cur.close()
    con.commit()
    con.close()

