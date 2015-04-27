#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Connects to the main database and creates tables
"""

from psycopg2 import connect

import common
import accident
import vehicle


user = common.get_user()
database = common.get_db_name()


con = connect(user=user, database=database)
cur = con.cursor()

cur.execute(accident.create_table_command())
cur.execute(vehicle.create_table_command())

cur.close()
con.commit()
con.close()

