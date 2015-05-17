#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Parsing FARS vehicle CSV files and putting them into DB

"""

import csv
import sys
import os
from db_api import person
from db_api import accident
from db_api import vehicle
from fars_person_mapper import FARSPersonMapper
from fars_accident_mapper import FARSAccidentMapper
from fars_vehicle_mapper import FARSVehicleMapper


if len(sys.argv) != 3:
    print('Usage: {0} <year> <fars_data_dir>'.format(sys.argv[0]))
    exit(1)

year = int(sys.argv[1])
data_dir = sys.argv[2]
accident_path = os.path.join(data_dir, '{0}_accident.csv'.format(year))
person_path = os.path.join(data_dir, '{0}_person.csv'.format(year))
vehicle_path = os.path.join(data_dir, '{0}_vehicle.csv'.format(year))
accident_file = open(accident_path, 'rt')
person_file = open(person_path, 'rt')
vehicle_file = open(vehicle_path, 'rt')

try:
    # Parse persons
    person_reader = csv.reader(person_file)
    first_row = next(person_reader)
    mapper = FARSPersonMapper(first_row, year)
    persons = []
    driver_by_veh = {}
    for row in person_reader:
        if mapper.valid(row):
            veh_id = mapper.veh_id(row)
            if veh_id not in driver_by_veh:
                driver_by_veh[veh_id] = None
            new_person = person.new(
                id=mapper.id(row),
                acc_id=mapper.acc_id(row),
                veh_id=veh_id,
                sex=mapper.sex(row),
                age=mapper.age(row),
                injury_level=mapper.injury_level(row),
                type=mapper.type(row),
                seatbelt=mapper.seatbelt(row),
                seated_pos=mapper.seated_pos(row)
            )
            persons.append(new_person)
            if new_person['type'] == 'DRIVER':
                driver_by_veh[veh_id] = new_person

    # Parse vehicles
    vehicle_reader = csv.reader(vehicle_file)
    first_row = next(vehicle_reader)
    mapper = FARSVehicleMapper(first_row, year)
    vehicles = []
    speed_limits_by_acc = {}
    surface_conds_by_acc = {}
    traffic_controls_by_acc = {}
    vehicles_by_acc = {}
    for row in vehicle_reader:
        if mapper.valid(row):
            veh_id = mapper.id(row)
            acc_id = mapper.acc_id(row)
            if acc_id not in vehicles_by_acc:
                vehicles_by_acc[acc_id] = []
            vehicles_by_acc[acc_id].append(veh_id)
            new_vehicle = vehicle.new(
                id=veh_id,
                acc_id=acc_id,
                driver_sex=mapper.driver_sex(row, driver_by_veh),
                driver_age=mapper.driver_age(row, driver_by_veh),
                passenger_count=mapper.passenger_count(row),
                type=mapper.type(row),
                make=mapper.make(row),
                model=mapper.model(row),
                fuel_type=mapper.fuel_type(row),
                hit_and_run=mapper.hit_and_run(row),
                skidded=mapper.skidded(row),
                rollover=mapper.rollover(row),
                jackknifing=mapper.jackknifing(row),
                first_impact_area=mapper.first_impact_area(row),
                maneuver=mapper.maneuver(row),
                prior_location=mapper.prior_location(row),
                driver_drinking=mapper.driver_drinking(row)
            )
            if year > 2009:
                if acc_id not in speed_limits_by_acc:
                    speed_limits_by_acc[acc_id] = []
                print("Append speed_lim: {0}".format(mapper.speed_limit(row)))
                speed_limits_by_acc[acc_id].append(mapper.speed_limit(row))
            if year > 2010:
                if acc_id not in surface_conds_by_acc:
                    surface_conds_by_acc[acc_id] = []
                print("Append surface_cond: {0}".format(mapper.surface_cond(row)))
                surface_conds_by_acc[acc_id].append(mapper.surface_cond(row))
            if year > 2010:
                if acc_id not in traffic_controls_by_acc:
                    traffic_controls_by_acc[acc_id] = []
                print("Append traffic_control: {0}".format(mapper.traffic_control(row)))
                traffic_controls_by_acc[acc_id].append(mapper.traffic_control(row))
            vehicles.append(new_vehicle)

    # Parse accidents
    accident_reader = csv.reader(accident_file)
    first_row = next(accident_reader)
    mapper = FARSAccidentMapper(first_row, year)
    accidents = []
    for row in accident_reader:
        if mapper.valid(row, vehicles_by_acc):
            new_accident = accident.new(
                id=mapper.id(row),
                country='USA',
                timestamp=mapper.timestamp(row),
                day_of_week=mapper.day_of_week(row),
                latitude=mapper.latitude(row),
                longitude=mapper.longitude(row),
                persons_count=mapper.persons_count(row),
                fatalities_count=mapper.fatalities_count(row),
                vehicles_count=mapper.vehicles_count(row, vehicles_by_acc),
                speed_limit=mapper.speed_limit(row, speed_limits_by_acc),
                snow=mapper.snow(row),
                rain=mapper.rain(row),
                wind=mapper.wind(row),
                fog=mapper.fog(row),
                relation_to_junction=mapper.relation_to_junction(row),
                road_class=mapper.road_class(row),
                surface_cond=mapper.surface_cond(row, surface_conds_by_acc),
                lighting=mapper.lighting(row),
                traffic_control=mapper.traffic_control(row, traffic_controls_by_acc),
                other_conditions=mapper.other_conditions(row)
            )
            accidents.append(new_accident)

    accident.insert(accidents)
    vehicle.insert(vehicles)
    person.insert(persons)

finally:
    person_file.close()
    accident_file.close()
    vehicle_file.close()