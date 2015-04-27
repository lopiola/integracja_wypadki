# -*- coding: utf-8 -*-

"""
Includes global definitions and common functions used across all scripts.
"""

import getpass

# Definitions used across all db_scripts
user = getpass.getuser()
database = 'accidents'


def get_user():
    return user


def get_db_name():
    return database


def check_key_constraints(data, constraints):
    for key in data.keys():
        if key in constraints:
            if not data[key] in constraints[key]:
                err_msg = 'Value {0} is not permitted for the attribute {1}'.format(data[key], key)
                raise ValueError(err_msg)