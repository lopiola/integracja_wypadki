#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Manipulates the accident table
"""

from psycopg2 import connect

import common

constraints = {
    'relation_to_junction': ['UNKNOWN'],
    'road_class': ['UNKNOWN'],
    'surface_cond': ['UNKNOWN'],
    'lighting': ['UNKNOWN'],
    'traffic_control': ['UNKNOWN'],
    'other_conditions': ['UNKNOWN']
}

def new(id,
        timestamp,
        day_of_week,
        latitude,
        longtitude,
        persons_count,
        fatalities_count,
        vehicles_count,
        speed_limit,
        snow=False,
        rain=False,
        wind=False,
        fog=False,
        relation_to_junction='UNKNOWN',
        road_class='UNKNOWN',
        surface_cond='UNKNOWN',
        lighting='UNKNOWN',
        traffic_control='UNKNOWN',
        other_conditions='UNKNOWN'):
    accident = {
        'id': id,
        'timestamp': timestamp,
        'day_of_week': day_of_week,
        'latitude': latitude,
        'longtitude': longtitude,
        'persons_count': persons_count,
        'fatalities_count': fatalities_count,
        'vehicles_count': vehicles_count,
        'speed_limit': speed_limit,
        'snow': snow,
        'rain': rain,
        'wind': wind,
        'fog': fog,
        'relation_to_junction': relation_to_junction,
        'road_class': road_class,
        'surface_cond': surface_cond,
        'lighting': lighting,
        'traffic_control': traffic_control,
        'other_conditions': other_conditions
    }

    for key in accident.keys():
        if key in constraints:
            if not accident[key] in constraints[key]:
                err_msg = 'Value {0} is not permitted for the attribute {1}'.format(accident[key], key)
                raise ValueError(err_msg)

    return accident


def add(accident_list):
    if not isinstance(accident_list, list):
        accident_list = [accident_list]
    user = common.get_user()
    database = common.get_db_name()
    con = connect(user=user, database=database)
    cur = con.cursor()

    for accident in accident_list:
        cur.execute(insert_command(accident))

    cur.close()
    con.commit()
    con.close()


def create_table_command():
    return '''
CREATE TABLE accident(
id                      INT PRIMARY KEY     NOT NULL,
timestamp               TIMESTAMPTZ         NOT NULL,
day_of_week             INT                 NOT NULL,
latitude                NUMERIC(13,10)      NOT NULL,
longtitude              NUMERIC(13,10)      NOT NULL,
persons_count           INT                 NOT NULL,
fatalities_count        INT                 NOT NULL,
vehicles_count          INT                 NOT NULL,
speed_limit             INT                 NOT NULL,
snow                    BOOLEAN             NOT NULL,
rain                    BOOLEAN             NOT NULL,
wind                    BOOLEAN             NOT NULL,
fog                     BOOLEAN             NOT NULL,
relation_to_junction    TEXT                NOT NULL,
road_class              TEXT                NOT NULL,
surface_cond            TEXT                NOT NULL,
lighting                TEXT                NOT NULL,
traffic_control         TEXT                NOT NULL,
other_conditions        TEXT                NOT NULL
);
'''


def insert_command(accident):
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
{speed_limit},
{snow},
{rain},
{wind},
{fog},
{relation_to_junction},
{road_class},
{surface_cond},
{lighting},
{traffic_control},
{other_conditions},
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
        speed_limit=accident['speed_limit'],
        snow=accident['snow'],
        rain=accident['rain'],
        wind=accident['wind'],
        fog=accident['fog'],
        relation_to_junction=accident['relation_to_junction'],
        road_class=accident['road_class'],
        surface_cond=accident['surface_cond'],
        lighting=accident['lighting'],
        traffic_control=accident['traffic_control'],
        other_conditions=accident['other_conditions']
    )
    return command