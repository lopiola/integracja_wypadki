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