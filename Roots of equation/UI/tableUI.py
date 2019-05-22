# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tableDesign.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAbstractScrollArea


class Ui_TableWindow(object):
    def setupUi(self, TableWindow):
        TableWindow.setObjectName("TableWindow")
        TableWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(TableWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.TableLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TableLabel.sizePolicy().hasHeightForWidth())
        self.TableLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.TableLabel.setFont(font)
        self.TableLabel.setObjectName("TableLabel")
        self.verticalLayout.addWidget(self.TableLabel)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        #self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget.setLineWidth(0)
        self.tableWidget.setEnabled(False)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.verticalLayout.addWidget(self.tableWidget)
        TableWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(TableWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        TableWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(TableWindow)
        self.statusbar.setObjectName("statusbar")
        TableWindow.setStatusBar(self.statusbar)

        self.retranslateUi(TableWindow)
        QtCore.QMetaObject.connectSlotsByName(TableWindow)

    def retranslateUi(self, TableWindow):
        _translate = QtCore.QCoreApplication.translate
        TableWindow.setWindowTitle(_translate("TableWindow", "Solution Table"))
        self.TableLabel.setText(_translate("TableWindow",
                                           "                                                                                                           TextLabel"))
