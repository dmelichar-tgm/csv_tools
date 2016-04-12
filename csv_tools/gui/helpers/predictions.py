from PySide import QtGui

from PySide.QtGui import QDialog, QVBoxLayout

from csv_tools.gui.csv_table_model import CSVTableModel


class PredictionsController(QDialog):

    def __init__(self, data, header, title, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        table_model = CSVTableModel(datalist=[], header=[], parent=self)
        table_model.set_list(data, header)

        self.view = QtGui.QTableView(self)
        self.view.setModel(table_model)
        self.view.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.view.resizeColumnsToContents()
        layout.addWidget(self.view)

        self.setWindowTitle(title)
        self.resize(850,120)
        self.setModal(True)
        # self.show()
        self.exec_()