#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module contains common function for FARS parsers
"""


def value_by_mapping(value, year, mapping):
    if value == -1:
        return 'UNKNOWN'
    default = mapping['default']
    all_keys = mapping.keys()
    all_keys.remove('default')
    all_keys.sort()
    from_year = 0
    for i in xrange(0, len(all_keys)):
        if year > all_keys[i]:
            from_year = all_keys[i]
    if from_year == 0:
        return 'UNKNOWN'
    branch = mapping[from_year]
    if value in branch:
        return branch[value]
    else:
        return default
