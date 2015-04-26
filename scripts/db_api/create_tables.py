#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Connects to the main database and creates tables
"""

from psycopg2 import connect

import common


user = common.get_user()
database = common.get_db_name()


con = connect(user=user, database=database)
cur = con.cursor()

cur.execute('''
CREATE TABLE accident(
id                  INT PRIMARY KEY     NOT NULL,
timestamp           TIMESTAMPTZ         NOT NULL,
day_of_week         INT                 NOT NULL,
latitude            NUMERIC(13,10)      NOT NULL,
longtitude          NUMERIC(13,10)      NOT NULL,
persons_count       INT                 NOT NULL,
fatalities_count    INT                 NOT NULL,
vehicles_count      INT                 NOT NULL,
speed_limit         INT                 NOT NULL
);
''')


cur.close()
con.commit()
con.close()

