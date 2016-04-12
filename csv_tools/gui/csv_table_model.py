#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
*************
CSVTableModel
*************

This is the Model that is being used for the GUI.
It holds all the functions and operations that you can
do with the Table.
"""
from PySide import QtCore

from PySide.QtCore import QAbstractTableModel, SIGNAL, QModelIndex, Qt

__author__ = "Daniel Melichar"
__copyright__ = "Copyright 2015"
__credits__ = ["Daniel Melichar"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Daniel Melichar"
__email__ = "dmelichar@student.tgm.ac.at"
__status__ = "Deployed"

class CSVTableModel(QAbstractTableModel):
    def __init__(self, parent, datalist, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.header = []
        self.list = []
        self.set_list(datalist, header)

    def set_list(self, datalist, header):
        self.emit(SIGNAL("layoutToBeChanged()"))
        self.list = datalist
        self.header = header
        self.emit(SIGNAL("layoutChanged()"))

    def get_list(self):
        return self.list

    def get_header(self):
        return self.header

    def rowCount(self, parent):
        return len(self.list)

    def columnCount(self, parent):
        return len(self.header)

    def duplicateRow(self, row_index, parent=QModelIndex()):
        self.beginInsertRows(parent, row_index, 1)
        row = self.list[row_index].copy()
        self.list.insert(row_index + 1, {key: "" for key in self.header})
        self.list[row_index + 1] = row
        self.endInsertRows()

    def insertRows(self, row, count, parent=QModelIndex()):
        self.beginInsertRows(parent, row, row + count - 1)
        for i in range(count):
            self.list.insert(row, {key: "" for key in self.header})
        self.endInsertRows()
        return True

    def removeRows(self, row, count, parent=QModelIndex()):
        self.beginRemoveRows(parent, row, row + count - 1)
        del self.list[row:row + count]
        self.endRemoveRows()
        return True

    def data(self, index, role=Qt.DisplayRole):
        """
        Returns the data stored under the given role for the item referred to by the index.

        :type index: Pyside.QtCore.QModelIndex
        :param index: Where is the data in general?
        :type role: Pyside.QtCore.int
        :param role: Where is it in our Model?
        :return
        """
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None

        return self.list[index.row()][self.header[index.column()]]

    def setData(self, *args, **kwargs):
        self.list[args[0].row()][self.header[args[0].column()]] = args[1]
        # self.emit(SIGNAL("dataChanged()"))
        return True

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable