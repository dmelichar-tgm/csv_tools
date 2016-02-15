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
try:
    from csv_tools.gui.helpers.about import AboutWindow
except:
    # I have no idea why this works, and the import above doesn't.
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../helpers/'))
    from about import AboutWindow

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
    windowList = []

    def __init__(self):
        super(MainWindow, self).__init__()

        self.recentFileActs = []

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.tableWidget = QtGui.QTableWidget()
        self.setCentralWidget(self.tableWidget)

        self.createActions()
        self.createMenus()
        self.statusBar()
        self.setStatusBarMessage(5, 10)

        self.setWindowTitle("CSV-Tools")
        self.resize(800, 400)
        self.move(30, 30)

    def newFile(self):
        other = MainWindow()
        MainWindow.windowList.append(other)
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
        pass # ToDo

    def redo(self):
        pass # ToDo

    def cut(self):
        pass # ToDo

    def copy(self):
        pass # ToDo

    def paste(self):
        pass # ToDo

    def bold(self):
        pass # ToDo

    def italic(self):
        pass # ToDo

    def setStatusBarMessage(self, x, y):
        location = "[{0}|{1}]".format(x, y)
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

        self.boldAct = QtGui.QAction("&Bold", self, checkable=True,
                shortcut="Ctrl+B", statusTip="Make the text bold",
                triggered=self.bold)

        boldFont = self.boldAct.font()
        boldFont.setBold(True)
        self.boldAct.setFont(boldFont)

        self.italicAct = QtGui.QAction("&Italic", self, checkable=True,
                shortcut="Ctrl+I", statusTip="Make the text italic",
                triggered=self.italic)

        italicFont = self.italicAct.font()
        italicFont.setItalic(True)
        self.italicAct.setFont(italicFont)

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

        self.fileMenu = self.menuBar().addMenu("&Edit")
        self.fileMenu.addAction(self.undoAct)
        self.fileMenu.addAction(self.redoAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.cutAct)
        self.fileMenu.addAction(self.copyAct)
        self.fileMenu.addAction(self.pasteAct)
        self.fileMenu.addSeparator()

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def loadFile(self, fileName):
        file = QtCore.QFile(fileName)
        if not file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "CSV-Tools",
                                      "Cannot read file %s:\n%s." % (fileName, file.errorString()))
            return

            # instr = QtCore.QTextStream(file)
            # QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            # self.textEdit.setPlainText(instr.readAll())
            # QtGui.QApplication.restoreOverrideCursor()
            #
            # self.setCurrentFile(fileName)
            # self.statusBar().showMessage("File loaded", 2000)

    def saveFile(self, fileName):
        file = QtCore.QFile(fileName)
        if not file.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "CSV-Tools",
                                      "Cannot write file %s:\n%s." % (fileName, file.errorString()))
            return

            # outstr = QtCore.QTextStream(file)
            # QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            # outstr << self.textEdit.toPlainText()
            # QtGui.QApplication.restoreOverrideCursor()
            #
            # self.setCurrentFile(fileName)
            # self.statusBar().showMessage("File saved", 2000)

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


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
