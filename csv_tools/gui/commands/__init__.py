#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
***********************
Commands with Undo/Redo
***********************

The following are all commands that have an undo/redo functionality.

Cudos: Mathias Ritter (5AHITM)
"""

from PySide.QtGui import QUndoCommand

__author__ = "Daniel Melichar"
__copyright__ = "Copyright 2015"
__credits__ = ["Daniel Melichar"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Daniel Melichar"
__email__ = "dmelichar@student.tgm.ac.at"
__status__ = "Deployed"

class EditCommand(QUndoCommand):
    def __init__(self, model, index):
        QUndoCommand.__init__(self)
        self.__newValue = None
        self.__model = model
        self.__index = index
        self.__oldValue = None

    def redo(self):
        self.__oldValue = self.__model.data(self.__index)
        self.__model.setData(self.__index, self.__newValue)

    def undo(self):
        self.__newValue = self.__model.data(self.__index)
        self.__model.setData(self.__index, self.__oldValue)

    def setText(self, *args, **kwargs):
        # noinspection PyCompatibility
        super().setText(*args, **kwargs)

    def newValue(self, newValue):
        self.__newValue = newValue


class InsertRowsCommand(QUndoCommand):
    def __init__(self, model, index, amount):
        QUndoCommand.__init__(self)
        self.__model = model
        self.__index = index
        self.__amount = amount

    def redo(self):
        self.__model.insertRows(self.__index, self.__amount)

    def undo(self):
        self.__model.removeRows(self.__index, self.__amount)


class RemoveRowsCommand(QUndoCommand):
    def __init__(self, model, index, amount):
        QUndoCommand.__init__(self)
        self.__model = model
        self.__index = index
        self.__amount = amount
        self.__oldList = None
        self.__oldHeader = None

    def redo(self):
        self.__oldHeader = self.__model.get_header()
        self.__oldList = self.__model.get_list()
        self.__model.removeRows(self.__index, self.__amount)

    def undo(self):
        self.__model.set_data(self.__oldList, self.__oldHeader)


class DuplicateRowCommand(QUndoCommand):
    def __init__(self, model, index):
        QUndoCommand.__init__(self)
        self.__model = model
        self.__index = index

    def redo(self):
        self.__model.duplicateRow(self.__index)

    def undo(self):
        self.__model.removeRows(self.__index, 1)