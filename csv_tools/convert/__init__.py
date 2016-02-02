#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module holds the code that is actually responsible
for converting any given file to a correct CSV.

At the moment the only two supported formats are XLSx and
a badly formatted CSV.
"""

from csv_tools.convert.bad_csv import bad_csv
from csv_tools.convert.xlsx import xlsx

__author__ = "Daniel Melichar"
__copyright__ = "Copyright 2015"
__credits__ = ["Daniel Melichar"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Daniel Melichar"
__email__ = "dmelichar@student.tgm.ac.at"
__status__ = "Deployed"

SUPPORTED_FORMATS = ['xlsx', 'csv']

def convert(f, format, schema=None, key=None, **kwargs):
    """
    Convert a file of a specified format to CSV.

    :param f: File that shall be converted (must not be None)
    :type f: File
    :param format: What the file shall be converted to (must not be None)
    :type format: String
    :returns: Correctly formatted CSV-File

    """

    if not f:
        raise ValueError('f must not be None')

    if not format:
        raise ValueError('format must not be None')


    if format == 'xlsx':
        return xlsx(f, **kwargs)
    elif format == 'csv':
        return bad_csv(f, **kwargs)
    else:
        raise ValueError('The format "%s" is not supported' % format)

def guess_format(filename):
    """
    Try to guess a file's format based on its extension (or lack thereof).
    """
    last_period = filename.rfind('.')

    if last_period == -1:
        # No extension: assume fixed-width
        return 'fixed'

    extension = filename[last_period + 1:].lower()

    if extension == 'xls':
        return extension
    elif extension == 'xlsx':
        return extension
    elif extension in ['json', 'js']:
        return 'json'
    elif extension == 'csv':
        return extension
    elif extension == 'fixed':
        return extension
    elif extension == 'dbf':
        return extension

    return None