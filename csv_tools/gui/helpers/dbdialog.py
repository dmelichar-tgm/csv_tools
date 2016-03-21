#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
*****************
File description
*****************

A File description that's a bit longer.
"""

from PySide import QtGui, QtCore

__author__ = "Daniel Melichar"
__copyright__ = "Copyright 2015"
__credits__ = ["Daniel Melichar"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Daniel Melichar"
__email__ = "dmelichar@student.tgm.ac.at"
__status__ = "Production"

class DatabaseDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(DatabaseDialog, self).__init__(parent)
        layout = QtGui.QFormLayout()

        self.dbms = QtGui.QPushButton("DBMS")
        self.dbms.clicked.connect(self.selectDBMS)
        self.dbms_choice = QtGui.QLabel()
        layout.addRow(self.dbms, self.dbms_choice)

        self.user_label = QtGui.QLabel("Username")
        self.user = QtGui.QLineEdit()
        layout.addRow(self.user_label, self.user)

        self.password_label = QtGui.QLabel("Password")
        self.password = QtGui.QLineEdit()
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        layout.addRow(self.password_label, self.password)

        self.host_label = QtGui.QLabel("Host")
        self.host = QtGui.QLineEdit()
        layout.addRow(self.host_label, self.host)

        self.port_label = QtGui.QLabel("Port")
        self.port = QtGui.QLineEdit()
        layout.addRow(self.port_label, self.port)

        self.db_label = QtGui.QLabel("Database")
        self.db = QtGui.QLineEdit()
        layout.addRow(self.db_label, self.db)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)
        self.setWindowTitle("Create connection")

    def dbms(self):
        return self.dbms_choice.text()

    def user(self):
        return self.user.text()

    def password(self):
        return self.password.text()

    def host(self):
        return self.host.text()

    def database(self):
        return self.db.text()

    def getAllValues(self):
        return {'dialect':self.dbms_choice.text(), 'username': self.user.text(), 'password': self.password.text(), 'host': self.host.text(), 'port': self.port.text(), 'database': self.db.text()}

    def selectDBMS(self):
        item, ok = QtGui.QInputDialog.getItem(self, "Select your DBMS", "List of supported DBMS", ['postgresql', 'mysql', 'sqllite'], 0, False)

        if ok and item:
            self.dbms_choice.setText(item)

    @staticmethod
    def getAll(parent = None):
        dialog = DatabaseDialog(parent)
        result = dialog.exec_()
        values = dialog.getAllValues()
        dialog.close()
        return (values, result == QtGui.QDialog.Accepted)