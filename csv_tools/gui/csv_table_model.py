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
import csv

from PySide import QtCore

from PySide.QtCore import QAbstractTableModel, SIGNAL, QModelIndex, Qt
from collections import Iterable

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

    def set_list(self, datalist, header=None):
        self.emit(SIGNAL("layoutToBeChanged()"))
        self.list = datalist
        if header is None:
            self.get_header()
        else:
            self.header = header
        self.emit(SIGNAL("layoutChanged()"))

    def get_list(self):
        return self.list

    def get_header(self):
        return self.header

    def rowCount(self, parent):
        return len(self.list)

    def open(self, path, clear=True):
        with open(path) as file:
            reader = CSVReader(file)
            if clear:
                self.list.clear()
            reader.collect(self.list)
        self.generate_headers()
        self.reset()

    def generate_headers(self):
        if len(self.list) > 0:
            self.header = []
            for key in self.list[0]:
                self.header.append(key)

    def save(self, path):
        with open(path, "w") as file:
            writer = CSVWriter(file)
            writer.writeAll(self.list)

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

class CSVReader(Iterable):
    def __iter__(self):
        dialect = csv.Sniffer().sniff(self.file.read(1024))
        self.file.seek(0)
        reader = csv.DictReader(self.file, dialect=dialect)
        for row in reader:
            newrow = {}
            for key, value in row.items():
                if key.strip() is not "":
                    newrow[key.strip()] = value
            yield newrow

    def collect(self, list=None):
        if list is None:
            list = []
        for item in self:
            list.append(item)
        return list

    def __init__(self, file):
        if file is None or not hasattr(file, 'read'):
            raise Exception("invalid file")
        self.file = file


    @staticmethod
    def write(filename, lines, delimiter=';'):

        with open(filename, 'w') as csvfile:

            if len(lines) == 0:
                return

            fieldnames = list(lines[0].keys())
            writer = csv.DictWriter(csvfile, delimiter=delimiter, fieldnames=fieldnames)
            writer.writerow(dict((fn, fn) for fn in fieldnames))

            for line in lines:
                writer.writerow(line)

class CSVWriter():
    def __init__(self, file):
        if file is None or not hasattr(file, 'write'):
            raise Exception("invalid file")
        self.file = file
        self.dictwriter = None

    def write(self, row):
        if not self.dictwriter:
            fieldnames = list(row.keys())
            self.dictwriter = csv.DictWriter(self.file, delimiter=";", fieldnames=fieldnames)
            self.dictwriter.writerow(dict((fn, fn) for fn in fieldnames))

        self.dictwriter.writerow(row)

    def writeAll(self, rows):
        for row in rows:
            self.write(row)