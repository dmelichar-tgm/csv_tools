#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Daniel Melichar"
__copyright__ = "Copyright 2015"
__credits__ = ["Daniel Melichar"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Daniel Melichar"
__email__ = "dmelichar@student.tgm.ac.at"
__status__ = "Deployed"


def make_default_headers(n):
    """
    Make a set of simple, default headers for files that are missing them.
    """
    return ['column%i' % (i + 1) for i in range(n)]