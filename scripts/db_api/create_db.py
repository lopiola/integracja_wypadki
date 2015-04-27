#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Connects to 'postgres' (default) DB and creates a database with name specified in common.py
"""

from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import common


user = common.get_user()
database = common.get_db_name()

con = connect(user=user, database='postgres')
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = con.cursor()

cur.execute('CREATE DATABASE ' + database)

cur.close()
con.close()


