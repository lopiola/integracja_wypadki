#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Manipulates the person table
"""

from psycopg2 import connect

import common

constraints = {
    'sex': ['MALE', 'FEMALE', 'UNKNOWN'],
    'injury_level': ['FATAL', 'SERIOUS', 'SLIGHT', 'NONE', 'UNKNOWN'],
    'type': ['DRIVER', 'PASSENGER', 'PEDESTRIAN', 'UNKNOWN'],
    'seatbelt': ['NOT_APPLICABLE', 'WORN_CONFIRMED', 'WORN_NOT_CONFIRMED', 'NOT_WORN', 'UNKNOWN'],
    'seated_pos': ['DRIVER', 'PASSENGER', 'BACK', 'UNKNOWN']
}


def new(id,
        acc_id,
        veh_id,
        sex,
        age,
        injury_level,
        type='UNKNOWN',
        seatbelt='UNKNOWN',
        seated_pos='UNKNOWN'):
    person = {
        'id': id,
        'acc_id': acc_id,
        'veh_id': veh_id,
        'sex': sex,
        'age': age,
        'injury_level': injury_level,
        'type': type,
        'seatbelt': seatbelt,
        'seated_pos': seated_pos,
    }

    common.check_key_constraints(person, constraints)
    return person


def insert(person_list):
    if not isinstance(person_list, list):
        person_list = [person_list]
    user = common.get_user()
    database = common.get_db_name()
    con = connect(user=user, database=database)
    cur = con.cursor()

    for person in person_list:
        cur.execute(insert_command(person))

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

    for person_id in id_list:
        cur.execute(delete_command(person_id))

    cur.close()
    con.commit()
    con.close()


def create_table_command():
    return '''
CREATE TABLE person(
id                      BIGINT PRIMARY KEY  NOT NULL,
acc_id                  BIGINT              NOT NULL,
veh_id                  BIGINT              NULL,
sex                     TEXT                NOT NULL,
age                     INT                 NOT NULL,
type                    TEXT                NOT NULL,
injury_level            TEXT                NOT NULL,
seatbelt                TEXT                NOT NULL,
seated_pos              TEXT                NOT NULL
);
'''


def insert_command(person):
    command = '''
INSERT INTO person VALUES (
{id},
{acc_id},
{veh_id},
'{sex}',
{age},
'{type}',
'{injury_level}',
'{seatbelt}',
'{seated_pos}'
);
'''
    command = command.format(
        id=person['id'],
        acc_id=person['acc_id'],
        veh_id=person['veh_id'],
        sex=person['sex'],
        age=person['age'],
        type=person['type'],
        injury_level=person['injury_level'],
        seatbelt=person['seatbelt'],
        seated_pos=person['seated_pos'],
    )
    return command


def delete_command(person_id):
    command = '''DELETE FROM person WHERE id = {id}'''
    return command.format(id=person_id)