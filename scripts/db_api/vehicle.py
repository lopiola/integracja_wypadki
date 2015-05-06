#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Manipulates the accident table
"""

from psycopg2 import connect

import common

constraints = {
    'type': ['UNKNOWN'],
    'make': ['UNKNOWN'],
    'model': ['UNKNOWN'],
    'fuel_type': ['UNKNOWN'],
    'hit_and_run': ['YES', 'NO', 'UNKNOWN'],
    'skidded': ['YES', 'NO', 'UNKNOWN'],
    'rollover': ['YES', 'NO', 'UNKNOWN'],
    'jackknifing': ['YES', 'NO', 'UNKNOWN'],
    'first_impact_area': ['UNKNOWN'],
    'maneuver': ['UNKNOWN'],
    'prior_location': ['UNKNOWN'],
    'driver_drinking': ['YES', 'NO', 'UNKNOWN']
}


def new(id,
        acc_id,
        driver_sex,
        driver_age,
        passenger_count,
        type='UNKNOWN',
        make='UNKNOWN',
        model='UNKNOWN',
        fuel_type='UNKNOWN',
        hit_and_run='UNKNOWN',
        skidded='UNKNOWN',
        rollover='UNKNOWN',
        jackknifing='UNKNOWN',
        first_impact_area='UNKNOWN',
        maneuver='UNKNOWN',
        prior_location='UNKNOWN',
        driver_drinking='UNKNOWN'):
    vehicle = {
        'id': id,
        'acc_id': acc_id,
        'driver_sex': driver_sex,
        'driver_age': driver_age,
        'passenger_count': passenger_count,
        'type': type,
        'make': make,
        'model': model,
        'fuel_type': fuel_type,
        'hit_and_run': hit_and_run,
        'skidded': skidded,
        'rollover': rollover,
        'jackknifing': jackknifing,
        'first_impact_area': first_impact_area,
        'maneuver': maneuver,
        'prior_location': prior_location,
        'driver_drinking': driver_drinking
    }

    common.check_key_constraints(vehicle, constraints)
    return vehicle


def new_from_dict(vehicle_data):
    vehicle = {
        'type': 'UNKNOWN',
        'make': 'UNKNOWN',
        'model': 'UNKNOWN',
        'fuel_type': 'UNKNOWN',
        'hit_and_run': 'UNKNOWN',
        'skidded': 'UNKNOWN',
        'rollover': 'UNKNOWN',
        'jackknifing': 'UNKNOWN',
        'first_impact_area': 'UNKNOWN',
        'maneuver': 'UNKNOWN',
        'prior_location': 'UNKNOWN',
        'driver_drinking': 'UNKNOWN'
    }
    vehicle.update(vehicle_data)

    # TODO: Check that compulsory fields exist

    common.check_key_constraints(vehicle, constraints)
    return vehicle


def insert(vehicle_list):
    if not isinstance(vehicle_list, list):
        vehicle_list = [vehicle_list]
    user = common.get_user()
    database = common.get_db_name()
    con = connect(user=user, database=database)
    cur = con.cursor()

    for vehicle in vehicle_list:
        print(vehicle)
        cur.execute(insert_command(vehicle))

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

    for veh_id in id_list:
        cur.execute(delete_command(veh_id))

    cur.close()
    con.commit()
    con.close()


def create_table_command():
    return '''
CREATE TABLE vehicle(
id                      BIGINT PRIMARY KEY  NOT NULL,
acc_id                  BIGINT              NOT NULL,
driver_sex              TEXT                NOT NULL,
driver_age              INT                 NOT NULL,
passenger_count         INT                 NOT NULL,
type                    TEXT                NOT NULL,
make                    TEXT                NOT NULL,
model                   TEXT                NOT NULL,
fuel_type               TEXT                NOT NULL,
hit_and_run             TEXT                NOT NULL,
skidded                 TEXT                NOT NULL,
rollover                TEXT                NOT NULL,
jackknifing             TEXT                NOT NULL,
first_impact_area       TEXT                NOT NULL,
maneuver                TEXT                NOT NULL,
prior_location          TEXT                NOT NULL,
driver_drinking         TEXT                NOT NULL
);
'''


def insert_command(vehicle):
    command = '''
INSERT INTO vehicle VALUES (
{id},
{acc_id},
'{driver_sex}',
{driver_age},
{passenger_count},
'{type}',
'{make}',
'{model}',
'{fuel_type}',
'{hit_and_run}',
'{skidded}',
'{rollover}',
'{jackknifing}',
'{first_impact_area}',
'{maneuver}',
'{prior_location}',
'{driver_drinking}'
);
'''
    command = command.format(
        id=vehicle['id'],
        acc_id=vehicle['acc_id'],
        driver_sex=vehicle['driver_sex'],
        driver_age=vehicle['driver_age'],
        passenger_count=vehicle['passenger_count'],
        type=vehicle['type'],
        make=vehicle['type'],
        model=vehicle['model'],
        fuel_type=vehicle['fuel_type'],
        hit_and_run=vehicle['hit_and_run'],
        skidded=vehicle['skidded'],
        rollover=vehicle['rollover'],
        jackknifing=vehicle['jackknifing'],
        first_impact_area=vehicle['first_impact_area'],
        maneuver=vehicle['maneuver'],
        prior_location=vehicle['prior_location'],
        driver_drinking=vehicle['driver_drinking']
    )
    return command


def delete_command(veh_id):
    command = '''DELETE FROM vehicle WHERE id = {id}'''
    return command.format(id=veh_id)