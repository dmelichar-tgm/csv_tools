#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
*******
Bad CSV
*******

Convert bad a badly formatted CSV to a good one.

This is using the function of the table file to
convert the CSV in a correct manner.
"""

import six

from csv_tools import table

__author__ = "Daniel Melichar"
__copyright__ = "Copyright 2015"
__credits__ = ["Daniel Melichar"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Daniel Melichar"
__email__ = "dmelichar@student.tgm.ac.at"
__status__ = "Deployed"

def bad_csv(f, **kwargs):
    """
    Convert a CSV into a new CSV by normalizing types and correcting for other anomalies.

    :param f: Badly formatted CSV-File
    :type f: File
    """
    tab = table.Table.from_csv(f, **kwargs)

    o = six.StringIO()
    output = tab.to_csv(o)
    output = o.getvalue()
    o.close()

    return output