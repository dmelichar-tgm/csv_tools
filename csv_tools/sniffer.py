#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
*******************
CSV Dialect Sniffer
*******************

This module goes through the common
delimiters and thereby tries to acknowledge the
CSV File's dialect
"""

import csv

__author__ = "Daniel Melichar"
__copyright__ = "Copyright 2015"
__credits__ = ["Daniel Melichar"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Daniel Melichar"
__email__ = "dmelichar@student.tgm.ac.at"
__status__ = "Deployed"


POSSIBLE_DELIMITERS = [',', '\t', ';', ' ', ':', '|']

def sniff_dialect(sample):
    """
    A functional version of ``csv.Sniffer().sniff``, that extends the
    list of possible delimiters to include some seen in the wild.
    """
    try:
        dialect = csv.Sniffer().sniff(sample, POSSIBLE_DELIMITERS)
    except:
        dialect = None

    return dialect
