#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Manipulates the accident table
"""

from psycopg2 import connect

import common

constraints = {
    'country': ['USA', 'GB'],
    'relation_to_junction': ['UNKNOWN', 'NON_JUNCTION', 'INTERSECTION', 'DRIVEWAY', 'RAMP'],
    'snow': ['YES', 'NO', 'UNKNOWN'],
    'rain': ['YES', 'NO', 'UNKNOWN'],
    'wind': ['YES', 'NO', 'UNKNOWN'],
    'fog': ['YES', 'NO', 'UNKNOWN'],
    'road_class': ['UNKNOWN', 'MOTORWAY', 'PRINCIPAL', 'MAJOR', 'MINOR', 'UNCLASSIFIED'],
    'surface_cond': ['UNKNOWN', 'DRY', 'WET', 'SNOW', 'ICE', 'FLOOD', 'OTHER'],
    'lighting': ['UNKNOWN', 'DAYLIGHT', 'DARK_LIGHTED', 'DARK'],
    'traffic_control': ['UNKNOWN', 'TRAFFIC_SIGNAL', 'SIGNAL_MALF', 'STOP_SIGN', 'YIELD_OR_NONE'],
    'other_conditions': ['UNKNOWN']
}


def new(id,
        country,
        timestamp,
        day_of_week,
        latitude,
        longitude,
        persons_count,
        fatalities_count,
        vehicles_count,
        speed_limit,
        snow='UNKNOWN',
        rain='UNKNOWN',
        wind='UNKNOWN',
        fog='UNKNOWN',
        relation_to_junction='UNKNOWN',
        road_class='UNKNOWN',
        surface_cond='UNKNOWN',
        lighting='UNKNOWN',
        traffic_control='UNKNOWN',
        other_conditions='UNKNOWN'):
    accident = {
        'id': id,
        'country': country,
        'timestamp': timestamp,
        'day_of_week': day_of_week,
        'latitude': latitude,
        'longitude': longitude,
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

    common.check_key_constraints(accident, constraints)
    return accident


def new_from_dict(accident_data):
    accident = {
        'snow': 'UNKNOWN',
        'rain': 'UNKNOWN',
        'wind': 'UNKNOWN',
        'fog': 'UNKNOWN',
        'relation_to_junction': 'UNKNOWN',
        'road_class': 'UNKNOWN',
        'surface_cond': 'UNKNOWN',
        'lighting': 'UNKNOWN',
        'traffic_control': 'UNKNOWN',
        'other_conditions': 'UNKNOWN'
    }

    accident.update(accident_data)

    # TODO: Check obligatory fields

    common.check_key_constraints(accident, constraints)
    return accident


def insert(accident_list):
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


def delete(id_list):
    if not isinstance(id_list, list):
        id_list = [id_list]
    user = common.get_user()
    database = common.get_db_name()
    con = connect(user=user, database=database)
    cur = con.cursor()

    for acc_id in id_list:
        cur.execute(delete_command(acc_id))

    cur.close()
    con.commit()
    con.close()


def select(acc_id, fields=None):
    """
    Selects specified data for the accident with acc_id.
    :param fields: List of names of fields to fetch. If None of empty, SELECT * is performed.
    """
    user = common.get_user()
    database = common.get_db_name()
    con = connect(user=user, database=database)
    cur = con.cursor()

    cur.execute(select_command(acc_id, fields))
    result = cur.fetchone()

    cur.close()
    con.commit()
    con.close()

    return result


def update(acc_id, field_values):
    """
    Updates the values of some fields of the accident with acc_id.
    :param field_values: dictionary of values to update. {field_name: new_value}.
    :return: tuple with field values or None if no acc_id is found in the database.
    """
    user = common.get_user()
    database = common.get_db_name()
    con = connect(user=user, database=database)
    cur = con.cursor()

    cur.execute(update_command(acc_id, field_values))

    cur.close()
    con.commit()
    con.close()


def set_field(acc_id, field, value):
    """
    Sets the value of a field for the accident with acc_id.
    """
    update(acc_id, {field: value})


def create_table_command():
    return '''
CREATE TABLE accident(
id                      BIGINT PRIMARY KEY  NOT NULL,
country                 TEXT                NOT NULL,
timestamp               TIMESTAMP           NOT NULL,
day_of_week             INT                 NOT NULL,
latitude                NUMERIC(13,10)      NOT NULL,
longitude               NUMERIC(13,10)      NOT NULL,
persons_count           INT                 NOT NULL,
fatalities_count        INT                 NOT NULL,
vehicles_count          INT                 NOT NULL,
speed_limit             INT                 NOT NULL,
snow                    TEXT                NOT NULL,
rain                    TEXT                NOT NULL,
wind                    TEXT                NOT NULL,
fog                     TEXT                NOT NULL,
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
'{country}',
{timestamp},
{day_of_week},
{latitude},
{longitude},
{persons_count},
{fatalities_count},
{vehicles_count},
{speed_limit},
'{snow}',
'{rain}',
'{wind}',
'{fog}',
'{relation_to_junction}',
'{road_class}',
'{surface_cond}',
'{lighting}',
'{traffic_control}',
'{other_conditions}'
);
'''
    command = command.format(
        id=accident['id'],
        country=accident['country'],
        timestamp=accident['timestamp'],
        day_of_week=accident['day_of_week'],
        latitude=accident['latitude'],
        longitude=accident['longitude'],
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


def delete_command(acc_id):
    command = '''DELETE FROM accident WHERE id = {id}'''
    return command.format(id=acc_id)


def select_command(acc_id, fields = None):
    command = '''SELECT {field_string} FROM accident WHERE id = {id}'''
    if not fields or len(fields) == 0:
        field_string = "*"
    else:
        field_string = ", ".join(fields)
    return command.format(id=acc_id, field_string=field_string)


def update_command(acc_id, fields):
    command = '''UPDATE accident SET {field_list} WHERE id = {id}'''

    field_list = ""
    for (field, value) in fields.items():
        field_list += get_field_update(field, value)

    return command.format(id=acc_id, field_list=field_list)


def get_field_update(field, value):
    field_normal = "{field} = {value}"
    field_string = "{field} = '{value}'"
    if isinstance(value, basestring):
        field_format = field_string
    else:
        field_format = field_normal
    return field_format.format(
        field=field,
        value=value
    )