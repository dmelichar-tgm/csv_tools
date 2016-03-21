#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
*****************
File description
*****************

A File description that's a bit longer.
"""

import six
import os
import sys

__author__ = "Daniel Melichar"
__copyright__ = "Copyright 2015"
__credits__ = ["Daniel Melichar"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Daniel Melichar"
__email__ = "dmelichar@student.tgm.ac.at"
__status__ = "Production"



class LazyFile(six.Iterator):
    """
    A proxy for a File object that delays opening it until
    a read method is called.
    Currently this implements only the minimum methods to be useful,
    but it could easily be expanded.
    """

    def __init__(self, init, *args, **kwargs):
        self.init = init
        self.f = None
        self._is_lazy_opened = False

        self._lazy_args = args
        self._lazy_kwargs = kwargs

    def __getattr__(self, name):
        if not self._is_lazy_opened:
            self.f = self.init(*self._lazy_args, **self._lazy_kwargs)
            self._is_lazy_opened = True

        return getattr(self.f, name)

    def __iter__(self):
        return self

    def close(self):
        self.f.close()
        self.f = None
        self._is_lazy_opened = False

    def __next__(self):
        if not self._is_lazy_opened:
            self.f = self.init(*self._lazy_args, **self._lazy_kwargs)
            self._is_lazy_opened = True

        return next(self.f)


def open_input_file(path):
    """
    Open the input file
    """
    if six.PY2:
        mode = 'rb'
        kwargs = {}
    else:
        mode = 'rt'
        kwargs = {'encoding': 'utf-8'}

        if not path or path == '-':
            f = sys.stdin
        else:
            (_, extension) = os.path.splitext(path)

            f = LazyFile(open, path, mode, **kwargs)

    return f
