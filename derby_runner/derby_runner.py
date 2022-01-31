import sys
import pandas
import PyQt5
import yaml
import h5py

import testfunction as xf

import PyQt5.QtWidgets as Wid
import pyarrow.feather as feather

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHeaderView

# ##############################################################################

def ymlread(x: str):
    mfile = open(x, "r")
    menusTxt: dict = yaml.safe_load(mfile)
    mfile.close()
    return (menusTxt)

test_number = xf.testfunction(3)
print(test_number)
test_two = xf.testclass.test_two(input_number=3)
print(test_two)
# ##############################################################################

# ##############################################################################
class pandasModel(QAbstractTableModel):

    def __init__(self, data: object) -> object:
        QAbstractTableModel.__init__(self)
        self._data = data

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self._data.iloc[index.row(), index.column()] = value
            return True
        return False

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole or role == Qt.EditRole:
                value = self._data.iloc[index.row(), index.column()]
                return str(value)
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]

# +++
class Window(Wid.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.fileName = None
        self.initUI()

    def initUI(self):

        stations_columns = ['StationID', 'sName', 'sDescription', 'TroopID', 'Primary\nAdultID',
                            'Secondary\nAdultID', 'Longitude', 'Latitude', 'EventID']
        self.df_stations = pandas.DataFrame(columns=stations_columns, index=[1, 2, 3, 4, 5])
        #        self.iconname = "D:/_Qt/img/py-qt.png"
        self.setWindowTitle("Derby Runner")
        left = 1000
        top = 1200
        width = 1870
        height = 1480
        self.setGeometry(left, top, width, height)

        menus_text = ymlread("/home/brickyard314/PycharmProjects/derby_runner/resources/dr_menus.yml")
        self.table = QTableView()
        self.mainnmenu = Wid.QMainWindow.menuBar(self)
        self.setCentralWidget(self.table)

        Qmodel = pandasModel(self.df_stations)
        self.table.setModel(Qmodel)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.menuBar = Wid.QMainWindow.menuBar(self)

        File = self.menuBar.addMenu("&File")

        New = File.addAction('&New')
        New.triggered.connect(lambda: self.newFileDialog())

        Open = File.addAction('&Open')
        Open.triggered.connect(lambda: self.openFileDialog())

        Save = File.addAction('&Save')
        Save.triggered.connect(lambda: self.saveFileDialog())

        Edit = self.menuBar.addMenu("&Edit")

        sshFile = "../resources/derby_runner.stylesheet"
        with open(sshFile, "r") as fh:
            self.setStyleSheet(fh.read())

        self.show()

    def newFileDialog(self):
        x = 1
        print(x)

    def openFileDialog(self,):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self,
                                                       caption="Open File",
                                                       directory= "../resources/",
                                                       filter="All Files (*);;Python Files (*.py)",
                                                       options=options)
        if self.fileName[0]:
            self.df_events = pandas.read_hdf(self.fileName, key="events")
#            print(df_events)
            self.model = pandasModel(self.df_events)
            self.table.setModel(self.model)
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.setCentralWidget(self.table)

    def saveFileDialog(self,):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getSaveFileName(self, 'Save File', '../resources/', "Python Files (*.py);;All Files (*)",
                                               options=QFileDialog.DontUseNativeDialog)
        if self.fileName[0]:
            self.df_events = self.df_events.astype(str)
            self.df_events.to_hdf(self.fileName, key='events', mode='w')
            return 0

if __name__ == "__main__":
    app = Wid.QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
