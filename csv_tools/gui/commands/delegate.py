#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
********
Delegate
********

The following is an implementation of Qt's QStyledItemDelegate for our use case.

*From the Qt Wiki:*
When displaying data from models in Qt item views, e.g., a PySide.QtGui.QTableView,
the individual items are drawn by a delegate. Also, when an item is edited, it provides
an editor widget, which is placed on top of the item view while editing takes place.
PySide.QtGui.QStyledItemDelegate is the default delegate for all Qt item views, and is
installed upon them when they are created.

The PySide.QtGui.QStyledItemDelegate class is one of the Model/View Classes and is part
of Qt’s model/view framework . The delegate allows the display and editing of items
to be developed independently from the model and view.

The data of items in models are assigned an Qt.ItemDataRole; each item can store
a PySide.QtCore.QVariant for each role. PySide.QtGui.QStyledItemDelegate implements
display and editing for the most common datatypes expected by users, including booleans,
integers, and strings.

The data will be drawn differently depending on which role they have in the model.
The following table describes the roles and the data types the delegate can handle
for each of them. It is often sufficient to ensure that the model returns appropriate
data for each of the roles to determine the appearance of items in views.


Cudos: Mathias Ritter (5AHITM)
"""

from PySide.QtGui import QStyledItemDelegate, QLineEdit
try:
    from csv_tools.gui.commands import EditCommand
except:
    import sys, os

    sys.path.append(os.path.dirname(os.path.realpath(__file__)))
    from commands import EditCommand


__author__ = "Daniel Melichar"
__copyright__ = "Copyright 2015"
__credits__ = ["Daniel Melichar"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Daniel Melichar"
__email__ = "dmelichar@student.tgm.ac.at"
__status__ = "Deployed"

class ItemDelegate(QStyledItemDelegate):
    def __init__(self, undoStack, undoText, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.undoStack = undoStack
        self.edit = None
        self.undoText = undoText

    def setModelData(self, editor, model, index):
        newValue = editor.text()
        self.edit.newValue(newValue)
        self.undoStack.beginMacro("Edit Cell")
        self.undoStack.push(self.edit)
        self.undoStack.endMacro()
        self.undoText()

    def editorEvent(self, event, model, option, index):
        self.edit = EditCommand(model, index)

    def createEditor(self, parent, option, index):
        return QLineEdit(parent)