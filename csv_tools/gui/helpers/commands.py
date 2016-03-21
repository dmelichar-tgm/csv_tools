#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
*****************
File description
*****************

A File description that's a bit longer.
"""
from PySide.QtGui import QUndoCommand

__author__ = "Daniel Melichar"
__copyright__ = "Copyright 2015"
__credits__ = ["Daniel Melichar"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Daniel Melichar"
__email__ = "dmelichar@student.tgm.ac.at"
__status__ = "Production"

class EditCommand(QUndoCommand):

    def __init__(self):

        QUndoCommand.__init__(self)
