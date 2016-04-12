"""
The GUI for CSV-Tools

With the GUI, you have all the options available to you as you do with the console commands.
It supports a connecting to a Database and reading the Information in there, an editor with functionalities that
you are used to from normal Desktop Applications (like Undo/Redo) and much much more.
"""

import sys
from PySide import QtGui

from csv_tools.gui.csv_table_controller import CSVTableController

__author__ = "Daniel Melichar"
__copyright__ = "Copyright 2015"
__credits__ = ["Daniel Melichar"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Daniel Melichar"
__email__ = "dmelichar@student.tgm.ac.at"
__status__ = "Deployed"

def launch_new_instance():
    app = QtGui.QApplication(sys.argv)
    controller = CSVTableController()
    controller.show_window()
    sys.exit(app.exec_())

# TODO: TEMPORARY, REMOVE ONCE DEPLOYED
if __name__ == "__main__":
    launch_new_instance()