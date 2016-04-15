#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
******************
CSVTableController
******************

The main file of the GUI which collects all the necessary pieces, puts
them together and adds the necessary functionality to them.
"""

import csv
import os
import sys

from PySide import QtGui, QtCore
from PySide.QtGui import QFileDialog, QUndoStack, QApplication

from csv_tools.gui.csv_table_view import Ui_MainWindow
from csv_tools.gui.csv_table_model import CSVTableModel

import numpy
from matplotlib import pyplot as plt


try:
    from csv_tools.gui.commands import RemoveRowsCommand, DuplicateRowCommand, InsertRowsCommand, EditCommand
    from csv_tools.gui.commands.delegate import ItemDelegate
    from csv_tools.gui.helpers.database import DatabaseManager
    from csv_tools.gui.helpers.about import AboutWindow
except:
    # I have no idea why this works, and the import above doesn't.
    import sys, os

    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'commands/'))
    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'helpers/'))
    from commands import RemoveRowsCommand, DuplicateRowCommand, InsertRowsCommand, EditCommand
    from commands.delegate import ItemDelegate
    from helpers.database import DatabaseManager
    from helpers.about import AboutWindow


__author__ = "Daniel Melichar"
__copyright__ = "Copyright 2015"
__credits__ = ["Daniel Melichar"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Daniel Melichar"
__email__ = "dmelichar@student.tgm.ac.at"
__status__ = "Deployed"

DATABASE = "wien_wahl"
USERNAME = "wadmin"
PASSWORD = "password"
HOST = "localhost"
WAHLTERMIN = "2015-10-11"
MANDATE = 100

class CSVTableController(QtGui.QMainWindow):

    # noinspection PyCompatibility
    def __init__(self, parent=None):
        super().__init__(parent)

        self.undo_stack = QUndoStack()
        self.statusBar()

        self.view = Ui_MainWindow()
        self.view.setupUi(self)
        self.view.tableView.setSortingEnabled(False)
        self.view.tableView.setItemDelegate(ItemDelegate(self.undo_stack, self.set_undo_redo_text))

        self.filename = None
        self.table_model = CSVTableModel(self, datalist=[], header=[])

        self.view.actionConnect.setEnabled(True)
        self.view.actionDisconnect.setEnabled(False)
        self.view.actionInsert.setEnabled(False)
        self.view.actionReceive.setEnabled(False)
        self.view.actionCalculate_Predictions.setEnabled(False)

        self.view.actionAbout_Qt.triggered.connect(self.about_qt)
        self.view.actionAbout.triggered.connect(self.about)
        self.view.actionConnect.triggered.connect(self.connect)
        self.view.actionDisconnect.triggered.connect(self.disconnect)
        self.view.actionInsert.triggered.connect(self.insert)
        self.view.actionReceive.triggered.connect(self.receive)
        self.view.actionCalculate_Predictions.triggered.connect(self.calculate_predictions)
        self.view.actionUndo.triggered.connect(self.undo)
        self.view.actionRedo.triggered.connect(self.redo)
        self.view.actionCopy.triggered.connect(self.copy)
        self.view.actionPaste.triggered.connect(self.paste)
        self.view.actionInsert_Row_s.triggered.connect(self.insert_rows)
        self.view.actionDuplicate_Row_s.triggered.connect(self.duplicate_rows)
        self.view.actionRemove_Row_s.triggered.connect(self.remove_rows)
        self.view.actionNew.triggered.connect(self.new)
        self.view.actionOpen.triggered.connect(self.open)
        self.view.actionSave.triggered.connect(self.save)
        self.view.actionSave_as.triggered.connect(self.save_as)

        self.db = None

    def show_window(self):
        self.setEnabled(True)
        self.show()
        self.raise_()

    def update_table_model(self, data, header):
        self.table_model.set_list(data, header)
        self.view.tableView.reset()
        self.view.tableView.setModel(self.table_model)

    def set_undo_redo_text(self):
        undo = "Undo"
        redo = "Redo"
        undo_text = self.undo_stack.undoText()
        redo_text = self.undo_stack.redoText()
        if undo_text:
            undo += " \"" + undo_text + "\""
        if redo_text:
            redo += " \"" + redo_text + "\""
        self.view.actionUndo.setText(undo)
        self.view.actionRedo.setText(redo)

    def get_selection(self):
        zero_column_selected_indexes = self.get_zero_column_selected_indexes()
        if not zero_column_selected_indexes:
            return self.table_model.rowCount(self), 1
        first_zero_column_selected_index = zero_column_selected_indexes[0]
        zero_column_selected_indexes = self.get_zero_column_selected_indexes()

        if not first_zero_column_selected_index or not first_zero_column_selected_index.isValid():
            return False
        startingrow = first_zero_column_selected_index.row()

        return startingrow, len(zero_column_selected_indexes)

    def get_zero_column_selected_indexes(self):
        selected_indexes = self.view.tableView.selectedIndexes()
        if not selected_indexes:
            return
        return [index for index in selected_indexes if not index.column()]

    def about_qt(self):
        QtGui.qApp.aboutQt()

    def about(self):
        self.about = AboutWindow()
        self.about.show()

    def connect(self):
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

        connection_string = 'mysql+mysqldb://{username}:{password}@{host}/{database}'.format(username=USERNAME,
                                                                                             password=PASSWORD,
                                                                                             host=HOST,
                                                                                             database=DATABASE)
        try:
            if self.db is None:
                self.db = DatabaseManager(connectionstring=connection_string, electiondate="2015-10-11")
                self.statusBar().showMessage("Successfully connected to database")
                self.view.actionConnect.setEnabled(False)
                self.view.actionDisconnect.setEnabled(True)
                self.view.actionInsert.setEnabled(True)
                self.view.actionReceive.setEnabled(True)
                self.view.actionCalculate_Predictions.setEnabled(True)
        except:
            QtGui.QMessageBox.critical(self, "Connection Error",  "Error connecting to Database:\n" + sys.exc_info()[0], QMessageBox.Close)

        QtGui.QApplication.restoreOverrideCursor()

    def disconnect(self):
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

        if self.db is not None:
            self.db.close()
            self.db = None
            self.view.actionConnect.setEnabled(True)
            self.view.actionDisconnect.setEnabled(False)
            self.view.actionInsert.setEnabled(False)
            self.view.actionReceive.setEnabled(False)
            self.view.actionCalculate_Predictions.setEnabled(False)
            self.statusBar().showMessage("Successfully disconnected from database")


        QtGui.QApplication.restoreOverrideCursor()

    def insert(self):
        if self.filename is None or len(self.table_model.get_list()) == 0:
            self.statusBar().showMessage("You need to have some data to insert")
            return

        try:
            current_list = self.table_model.get_list()
            self.db.write(current_list)
        except Exception as e:
            print(e)
            self.statusBar().showMessage("Error while accessing the database.")

    def receive(self):
        try:
            data = self.db.load()
            self.table_model.set_list(data)
            self.update_table_model(self.table_model.get_list(), self.table_model.get_header())
        except Exception as e:
            print(e)
            self.statusBar().showMessage("Error while accessing the database.")

    def calculate_predictions(self):
        """
        Cudos an Rene Hollander
        """
        projection_data = self.db.create_projection()
        print("Hochrechnung:")
        for key, value in projection_data.items():
            print(key + ": " + str(value))
        print("\n")
        ind = numpy.arange(len(projection_data))
        width = 0.5
        plt.bar(ind, list(projection_data.values()), width, color='r')
        plt.ylabel('%')
        plt.xlabel('Parteien')
        plt.title('Wien Wahl Hochrechnung')
        plt.xticks(ind + width / 2, list(projection_data.keys()))
        plt.yticks(numpy.arange(0, 61, 5))
        plt.show()

    def undo(self):
        self.undo_stack.undo()
        self.set_undo_redo_text()
        self.view.tableView.reset()

    def redo(self):
        self.undo_stack.redo()
        self.set_undo_redo_text()
        self.view.tableView.reset()

    def copy(self):
        if len(self.view.tableView.selectionModel().selectedIndexes()) == 0:
            return

        clipboard = QApplication.clipboard()
        selected_index = self.view.tableView.selectionModel().selectedIndexes()[0]
        selected_text = str(self.table_model.data(selected_index))
        clipboard.setText(selected_text)

    def paste(self):
        if len(self.view.tableView.selectionModel().selectedIndexes()) == 0:
            return

        clipboard = QApplication.clipboard()
        index = self.view.tableView.selectionModel().selectedIndexes()[0]
        command = EditCommand(self.table_model, index)
        command.newValue(str(clipboard.text()))

        self.undo_stack.beginMacro("Paste")
        self.undo_stack.push(command)
        self.undo_stack.endMacro()
        self.set_undo_redo_text()
        self.view.tableView.reset()

    def insert_rows(self):
        if len(self.table_model.get_header()) == 0:
            self.statusBar().showMessage("Adding rows to an empty table without a header is not possible.")
            return
        start, amount = self.get_selection()

        self.undo_stack.beginMacro("Add Row")
        self.undo_stack.push(InsertRowsCommand(self.table_model, start, 1))
        self.undo_stack.endMacro()
        self.set_undo_redo_text()

    def duplicate_rows(self):
        if len(self.view.tableView.selectionModel().selectedIndexes()) == 0:
            self.statusBar().showMessage("You must select the first column of the row you want to duplicate")
            return

        start, amount = self.get_selection()
        self.undo_stack.beginMacro("Duplicate Row")
        self.undo_stack.push(DuplicateRowCommand(self.table_model, start))
        self.undo_stack.endMacro()
        self.set_undo_redo_text()
        self.view.tableView.reset()

    def remove_rows(self):
        if len(self.table_model.get_list()) == 0:
            self.statusBar().showMessage("WARNING: Removing rows from an empty table is not possible")
            return
        start, amount = self.get_selection()
        if start != len(self.table_model.get_list()):
            self.undo_stack.beginMacro("Remove Row(s)")
            self.undo_stack.push(RemoveRowsCommand(self.table_model, start, amount))
            self.undo_stack.endMacro()
            self.set_undo_redo_text()
        else:
            self.statusBar().showMessage("WARNING: You need to choose the rows you want to remove by selecting the cells in the "
                                   "first column")

    def new(self):
        if self.filename is not None:
            save = self.show_new_file_dialog()
            if(save):
                self.save()
                self.filename = None
                self.table_model.set_list([], [])
            else:
                self.filename = None
                self.table_model.set_list([], [])
        else:
            self.filename = None
            self.table_model.set_list([], [])

    def show_append_override_dialog(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("Append or Override")
        msgBox.setText("Append or override the current entries?")
        msgBox.addButton("Append", QtGui.QMessageBox.YesRole)
        msgBox.addButton("Override", QtGui.QMessageBox.NoRole)
        return msgBox.exec_()

    def show_new_file_dialog(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("New file")
        msgBox.setText("Do you want to save first?")
        msgBox.addButton("Yes", QtGui.QMessageBox.YesRole)
        msgBox.addButton("No", QtGui.QMessageBox.NoRole)
        return msgBox.exec_()

    def open(self):
        try:
            fileName = QFileDialog.getOpenFileName(self, self.tr("Open CSV File"), os.getcwd(),
                                                   self.tr("CSV Files (*.csv)"))[0]
            if fileName is not None and fileName is not "":
                append_or_override = False
                if self.filename is not None:
                    append_or_override = self.show_append_override_dialog()
                self.filename = fileName
                self.table_model.open(self.filename, clear=append_or_override)
                self.undo_stack.clear()
                self.set_undo_redo_text()
                self.update_table_model(self.table_model.get_list(), self.table_model.get_header())
        except FileNotFoundError:
            QtGui.QMessageBox.critical(self, "Read Error",
                                 "Error reading CSV File:\nFile \"" + self.filename + "\" not found!",
                                 QtGui.QMessageBox.Close)
        except csv.Error:
            QtGui.QMessageBox.critical(self, "Read Error", "Error reading CSV File:\n File is not an valid CSV File!",
                                 QtGui.QMessageBox.Close)
        except:
            QtGui.QMessageBox.critical(self, "Read Error", "Error reading CSV File:\nAn unknown Error occured!",
                                 QtGui.QMessageBox.Close)
            raise

    def save(self):
        if self.filename is not None and self.filename is not "":
            self.table_model.save(self.filename)
        else:
            fileName = QFileDialog.getSaveFileName(self, caption="Save CSV File", dir=os.getcwd(),
                                                   filter="CSV Files (*.csv)")[0]
            if fileName is not None and fileName is not "":
                self.table_model.save(fileName)

    def save_as(self):
        fileName = QFileDialog.getSaveFileName(self, caption="Save CSV File", dir=os.getcwd(), filter="CSV Files (*.csv)")[0]
        if fileName is not None and fileName is not "":
            self.table_model.save(fileName)