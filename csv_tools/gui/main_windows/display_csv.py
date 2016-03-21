#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**************************
Main Window of Application
**************************

This is the implementation of the UI File in Python.

"""

# This is only needed for Python v2 but is harmless for Python v3.
# import sip
# sip.setapi('QString', 2)
# sip.setapi('QVariant', 2)

from PySide import QtCore, QtGui
from csv_tools import table
from csv_tools import sql

try:
    import csv_tools.gui.helpers.about
    import csv_tools.gui.helpers.files
    import csv_tools.gui.helpers.dbdialog
except:
    # I have no idea why this works, and the import above doesn't.
    import sys, os

    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../helpers/'))
    from about import AboutWindow
    import files as FileHelper
    from dbdialog import DatabaseDialog

__author__ = "Daniel Melichar"
__copyright__ = "Copyright 2015"
__credits__ = ["Daniel Melichar"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Daniel Melichar"
__email__ = "dmelichar@student.tgm.ac.at"
__status__ = "Production"


class MainWindow(QtGui.QMainWindow):
    MaxRecentFiles = 5

    def __init__(self):
        super(MainWindow, self).__init__()

        self.recentFileActs = []

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.setCentralWidget(QtGui.QTableWidget())

        self.createActions()
        self.createMenus()
        self.statusBar()

        self.setWindowTitle("CSV-Tools")
        self.resize(800, 400)
        self.move(30, 30)

    def newFile(self):
        other = MainWindow()
        other.show()

    def open(self):
        fileName, filtr = QtGui.QFileDialog.getOpenFileName(self)
        if fileName:
            self.loadFile(fileName)

    def save(self):
        if self.curFile:
            self.saveFile(self.curFile)
        else:
            self.saveAs()

    def saveAs(self):
        fileName, filtr = QtGui.QFileDialog.getSaveFileName(self)
        if fileName:
            self.saveFile(fileName)

    def openRecentFile(self):
        action = self.sender()
        if action:
            self.loadFile(action.data())

    def about(self):
        self.about = AboutWindow()
        self.about.show()

    def undo(self):
        pass  # ToDo

    def redo(self):
        pass  # ToDo

    def cut(self):
        current = self.tableWidget.currentItem()
        clipboard = QtGui.QApplication.clipboard()
        clipboard.setText(current.text())
        current.setText('')

    def copy(self):
        current = self.tableWidget.currentItem()
        clipboard = QtGui.QApplication.clipboard()
        clipboard.setText(current.text())

    def paste(self):
        current = self.tableWidget.currentItem()
        clipboard = QtGui.QApplication.clipboard()
        current.setText(clipboard.text())

    def newRow(self):
        self.tableWidget.insertRow(self.tableWidget.rowCount())

    def duplicateRow(self):
        currentRow = self.tableWidget.currentRow()

        for column in range(self.tableWidget.columnCount()):
            str = self.tableWidget.itemAt(currentRow, column).text()
            print(str, column, currentRow)


        # print(self.tableWidget.itemAt(9,1).text()) #spo = 27

        # self.tableWidget.insertRow(self.tableWidget.rowCount())
        #
        # for item in range(self.tableWidget.columnCount()):
        #     dCell = self.tableWidget.itemAt(currentRow, item + 1)
        #     print(dCell.text(), item+1, currentRow)
        #     nCell = self.tableWidget.itemAt(self.tableWidget.rowCount(), item+1)
        #     nCell.setText(dCell.text())



    def establishConnection(self):
        dlg = DatabaseDialog()
        if dlg.exec_():
            QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            connection_string = '{dialect}://{username}:{password}@{host}:{port}/{database}'.format(**dlg.getAllValues())
            self.engine, self.metaData = sql.get_connection(connection_string)
            self.connection = self.engine.connect()

            self.metaData.reflect(self.engine) # Reflection needed since we didn't create the tables with SQLAlchemy
            print(self.metaData.tables.keys()) # Table Names
            # Load table and stuff
            #result = self.connection.execute("select * from partei")
            #print(result)


            self.break_connection.setEnabled(True)
            self.establish_connection.setDisabled(True)
            self.statusBar().showMessage("Connected to {dialect} Database: {database}".format(**dlg.getAllValues()))
            QtGui.QApplication.restoreOverrideCursor()

    def breakConnection(self):
        self.connection.close()
        #self.engine.drop()
        self.break_connection.setDisabled(True)
        self.establish_connection.setEnabled(True)
        self.statusBar().showMessage("Disconnected from database")

    def setStatusBarMessage(self):
        location = "[{0}|{1}]".format(self.tableWidget.currentRow()+1, self.tableWidget.currentColumn()+1)
        self.statusBar().showMessage(location)

    def createActions(self):
        self.newAct = QtGui.QAction("&New", self,
                                    shortcut=QtGui.QKeySequence.New,
                                    statusTip="Create a new file", triggered=self.newFile)

        self.openAct = QtGui.QAction("&Open...", self,
                                     shortcut=QtGui.QKeySequence.Open,
                                     statusTip="Open an existing file", triggered=self.open)

        self.saveAct = QtGui.QAction("&Save", self,
                                     shortcut=QtGui.QKeySequence.Save,
                                     statusTip="Save the document to disk", triggered=self.save)

        self.saveAsAct = QtGui.QAction("Save &As...", self,
                                       shortcut=QtGui.QKeySequence.SaveAs,
                                       statusTip="Save the document under a new name",
                                       triggered=self.saveAs)

        for i in range(MainWindow.MaxRecentFiles):
            self.recentFileActs.append(
                QtGui.QAction(self, visible=False,
                              triggered=self.openRecentFile))

        self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",
                                     statusTip="Exit the application",
                                     triggered=QtGui.qApp.closeAllWindows)

        self.undoAct = QtGui.QAction("&Undo", self,
                                     shortcut=QtGui.QKeySequence.Undo,
                                     statusTip="Undo the last operation", triggered=self.undo)

        self.redoAct = QtGui.QAction("&Redo", self,
                                     shortcut=QtGui.QKeySequence.Redo,
                                     statusTip="Redo the last operation", triggered=self.redo)

        self.cutAct = QtGui.QAction("Cu&t", self,
                                    shortcut=QtGui.QKeySequence.Cut,
                                    statusTip="Cut the current selection's contents to the clipboard",
                                    triggered=self.cut)

        self.copyAct = QtGui.QAction("&Copy", self,
                                     shortcut=QtGui.QKeySequence.Copy,
                                     statusTip="Copy the current selection's contents to the clipboard",
                                     triggered=self.copy)

        self.pasteAct = QtGui.QAction("&Paste", self,
                                      shortcut=QtGui.QKeySequence.Paste,
                                      statusTip="Paste the clipboard's contents into the current selection",
                                      triggered=self.paste)

        self.new_row = QtGui.QAction("New Row", self,
                                     statusTip="Add a new row to the table",
                                     triggered=self.newRow)

        self.duplicate_row = QtGui.QAction("Duplicate Row", self,
                                     statusTip="Duplicate a selected row",
                                     triggered=self.duplicateRow)

        self.establish_connection = QtGui.QAction("Connect to..", self,
                                     statusTip="Connect to a database",
                                     triggered=self.establishConnection)

        self.break_connection = QtGui.QAction("Disconnect from..", self,
                                     statusTip="Disconnect from the current database",
                                     triggered=self.breakConnection)

        self.break_connection.setDisabled(True)

        self.aboutAct = QtGui.QAction("&About", self,
                                      statusTip="Show the application's About box",
                                      triggered=self.about)

        self.aboutQtAct = QtGui.QAction("About &Qt", self,
                                        statusTip="Show the Qt library's About box",
                                        triggered=QtGui.qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.separatorAct = self.fileMenu.addSeparator()
        for i in range(MainWindow.MaxRecentFiles):
            self.fileMenu.addAction(self.recentFileActs[i])
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)
        self.updateRecentFileActions()

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.undoAct)
        self.editMenu.addAction(self.redoAct)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.cutAct)
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.pasteAct)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.new_row)
        self.editMenu.addAction(self.duplicate_row)

        self.dbMenu = self.menuBar().addMenu("&Database")
        self.dbMenu.addAction(self.establish_connection)
        self.dbMenu.addAction(self.break_connection)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def loadFile(self, fileName):
        fileEnding = fileName.split(".")[-1]
        file = QtCore.QFile(fileName)
        if not file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text) or fileEnding != 'csv' :
            if fileEnding != 'csv':
                QtGui.QMessageBox.warning(self, "CSV-Tools", "Cannot read file %s:\nYou must select a .csv file." % (fileName))
            else:
                QtGui.QMessageBox.warning(self, "CSV-Tools", "Cannot read file %s:\n%s." % (fileName, file.errorString()))
            return

        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

        f = FileHelper.open_input_file(path=fileName)
        table_name = os.path.splitext(os.path.split(f.name)[1])[0]
        csv_table = table.Table.from_csv(f, name=table_name)
        f.close()

        colcnt = len(csv_table.headers())-1
        rowcnt = csv_table.count_rows()
        self.tableWidget = QtGui.QTableWidget(rowcnt, colcnt)

        vheader = QtGui.QHeaderView(QtCore.Qt.Orientation.Vertical)
        vheader.setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.tableWidget.setVerticalHeader(vheader)
        hheader = QtGui.QHeaderView(QtCore.Qt.Orientation.Horizontal)
        hheader.setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.tableWidget.setHorizontalHeader(hheader)
        self.headers = [x.strip(' ') for x in csv_table.headers()] # remove spaces
        self.headers = [x for x in self.headers if x is not None] # remove None
        self.tableWidget.setHorizontalHeaderLabels(self.headers)

        for i in range(rowcnt):
            for j in range(colcnt):
                item = QtGui.QTableWidgetItem(str(csv_table.row(i)[j]))
                if item.text() != 'None':
                    self.tableWidget.setItem(i, j, item)
                    self.tableWidget.itemAt(i, j).setText(item.text()) # I have no idea why Qt doesn't do this when using setItem()

        self.tableWidget.itemSelectionChanged.connect(self.setStatusBarMessage)
        self.setCentralWidget(self.tableWidget)
        self.repaint()
        QtGui.QApplication.restoreOverrideCursor()
        self.setCurrentFile(fileName)
        self.statusBar().showMessage("File loaded", 2000)

    def saveFile(self, fileName):
        file = QtCore.QFile(fileName)
        if not file.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "CSV-Tools", "Cannot write file %s:\n%s." % (fileName, file.errorString()))
            return

        tableDisplay = table.Table(name=file)
        all_rows = self.tableWidget.rowCount()
        all_columns = self.tableWidget.columnCount()

        for row in range(0, all_rows):
            for column in xrange(0, all_columns):
                tableDisplay.insert(row, self.tableWidget.item(row, column))

    def setCurrentFile(self, fileName):
        self.curFile = fileName
        if self.curFile:
            self.setWindowTitle("%s - CSV-Tools" % self.strippedName(self.curFile))
        else:
            self.setWindowTitle("CSV-Tools")

        settings = QtCore.QSettings('', 'CSV-Tools')
        files = list(settings.value('recentFileList', []))

        try:
            files.remove(fileName)
        except ValueError:
            pass

        files.insert(0, fileName)
        del files[MainWindow.MaxRecentFiles:]

        settings.setValue('recentFileList', files)

        for widget in QtGui.QApplication.topLevelWidgets():
            if isinstance(widget, MainWindow):
                widget.updateRecentFileActions()

    def updateRecentFileActions(self):
        settings = QtCore.QSettings('', 'CSV-Tools')
        files = settings.value('recentFileList')

        files_no = 0
        if files:
            files_no = len(files)

        numRecentFiles = min(files_no, MainWindow.MaxRecentFiles)

        for i in range(numRecentFiles):
            text = "&%d %s" % (i + 1, self.strippedName(files[i]))
            self.recentFileActs[i].setText(text)
            self.recentFileActs[i].setData(files[i])
            self.recentFileActs[i].setVisible(True)

        for j in range(numRecentFiles, MainWindow.MaxRecentFiles):
            self.recentFileActs[j].setVisible(False)

        self.separatorAct.setVisible((numRecentFiles > 0))

    def strippedName(self, fullFileName):
        return QtCore.QFileInfo(fullFileName).fileName()

def launch_new_instance():
    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    launch_new_instance()