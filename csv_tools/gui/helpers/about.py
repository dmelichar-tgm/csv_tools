#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
************
About Window
************

It basically reads the README and displays it
"""

# This is only needed for Python v2 but is harmless for Python v3.
# import sip
# sip.setapi('QString', 2)
# sip.setapi('QVariant', 2)

from PySide import QtCore, QtGui
from docutils.core import publish_parts

__author__ = "Daniel Melichar"
__copyright__ = "Copyright 2015"
__credits__ = ["Daniel Melichar"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Daniel Melichar"
__email__ = "dmelichar@student.tgm.ac.at"
__status__ = "Production"

readme_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../../README.rst')

class AboutWindow(QtGui.QMainWindow):
    def __init__(self):
        super(AboutWindow, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        readme_rst = open(readme_path).read()
        readme_html = publish_parts(readme_rst, writer_name='html')['html_body']

        self.about = QtGui.QTextEdit(self)
        self.about.setHtml(readme_html)

        self.setCentralWidget(self.about)

        self.setWindowTitle("CSV-Tools: About")
        self.resize(500, 600)


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    about = AboutWindow()
    about.show()
    sys.exit(app.exec_())
