from PyQt5 import QtWidgets, QtCore

from tableUI import Ui_TableWindow

import sys
from decimal import *


class SolutionTable(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_TableWindow()
        self.method = None
        self.ui.setupUi(self)

    def fill_table(self, method):

        self.method = method
        name = self.method.method_name()
        print("table")
        if name == "secant":
            print("enter table")
            self.construct_table(("x(i-1)", "X(i)", "X(i+1)", "F(Xi)", "F(Xi-1)", "error(%)="))
        elif name == "fixed point":
            self.construct_table(("xr_prev", "xr", "absolute error"))
        elif name == "bisection":
            self.construct_table(("xu", "xl", "Xr", "F(Xr)",
                                  "F(self.xl)", "Error"))
        elif name == "false position":
            self.construct_table(("xu", "xl", "Xr", "F(Xr)",
                                  "F(xl)", "F(xu)", "Error"))
        elif name == "newton":
            self.construct_table(("xi", "xi+1", "F(xi)", "F'(xi)",
                                  "Error"))
        elif name == "general":
            print("sdfkjkfsdn")
            self.construct_table(("xa", "xb", "Xr", "F(Xr)", "F(xb1)",
                                     "F(xb2)", "Error"))

        return

    def construct_table(self, header_list):
        print("sjkvnxck")
        self.ui.tableWidget.setRowCount(self.method.get_taken_iteration())
        table = self.method.get_table()
        print(table)
        num_col = len(header_list)
        self.ui.tableWidget.setColumnCount(num_col)
        self.ui.tableWidget.setHorizontalHeaderLabels(header_list)
        for row in range(len(table)):
            for col in range(num_col):
                cell = QtWidgets.QTableWidgetItem(str(table[row][col]))
                print("entered")
                self.ui.tableWidget.setItem(row, col, cell)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    win = SolutionTable()

    win.show()

    sys.exit(app.exec())
